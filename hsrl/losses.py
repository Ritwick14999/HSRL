"""Structural losses for Stage I.

Interface (so new structural losses, e.g. interval / supported-ordering / joint four-image, plug in
without touching the training loop):
    loss_fn(z, tuples, meta) -> (scalar loss, per-tuple log dict of 1-D tensors)
      z       (B, D) normalised embeddings of the labelled mini-batch (with grad)
      tuples  dict of index tensors 'a', 'p', 'n', 'c' into the batch (from hsrl/mining.py)
      meta    dict with 'labels' (B,) and, for vote-aware losses (needs_votes = True), the tuples' labelled-set votes
              built by hsrl/stages.py: 'L', 'U' {pair: (T,)} agreement bounds for the vote mode, 'q', 'k', 'R'
              {role: (T,)} vote fraction, SSA/G4 votes and readers, 'gen' a torch.Generator for random controls
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .agreement import PAIR_ROLES, joint_agreements

CERT_EPS = 1e-6   # bounds come from vote fractions; equal bounds must not certify an ordering through rounding


def sq_dist(x, y):
    """Squared Euclidean distance between paired rows (Eq. 4)."""
    return ((x - y) ** 2).sum(-1)


def hsrl_hinges(z, tuples, alpha, beta, gamma):
    """The four tuple distances and HSRL's three hinges (Eq. 5), per tuple."""
    za, zp, zn, zc = (z[tuples[k]] for k in ("a", "p", "n", "c"))
    d_ap, d_an, d_nc, d_ac = sq_dist(za, zp), sq_dist(za, zn), sq_dist(zn, zc), sq_dist(za, zc)
    return {"d_ap": d_ap, "d_an": d_an, "d_nc": d_nc, "d_ac": d_ac, "t1": F.relu(d_ap - d_an + alpha),
            "t2": F.relu(d_ap - d_nc + beta), "t3": F.relu(d_ap - d_ac + gamma)}


class HSRLLoss(nn.Module):
    """Eq. 5:  max(0, d_ap - d_an + alpha) + max(0, d_ap - d_nc + beta) + max(0, d_ap - d_ac + gamma).
    `terms` selects which hinges are included (e.g. [1, 3] = HSRL without term 2). Mean over tuples."""

    def __init__(self, alpha=1.0, beta=0.5, gamma=0.5, terms=(1, 2, 3)):
        super().__init__()
        self.alpha, self.beta, self.gamma = alpha, beta, gamma
        self.terms = set(terms)

    def forward(self, z, tuples, meta=None):
        log = hsrl_hinges(z, tuples, self.alpha, self.beta, self.gamma)
        per = sum(log[f"t{i}"] for i in (1, 2, 3) if i in self.terms)
        if not torch.is_tensor(per):
            per = torch.zeros_like(log["d_ap"])
        log["loss"] = per
        return per.mean(), {k: v.detach() for k, v in log.items()}


class SupportedOrderingLoss(nn.Module):
    """Supervisor's plan §3, "supported ordering rather than assumed ordering". HSRL's term k imposes an ordering of
    reader agreement (term 1: s_ap > s_an, term 2: s_ap > s_nc, term 3: s_ap > s_ac, as in the census). A hinge is
    kept only where the annotations guarantee its ordering, L_x > U_y (bounds from the vote mode: counts-only Fréchet
    bounds, or the observed agreement of linked readers); undecided and contradicted orderings are omitted. Margins
    stay alpha / beta / gamma and the mean is over tuples, so a kept hinge has exactly HSRL's gradient (D45).
    select: 'certified' (the method) | 'random' (control: the same number of hinges per term and batch, at random) |
    'confidence' (control: the same number, from the tuples whose term images have the most extreme votes).
    margin (D47, plan §3: "the guaranteed gap is not an embedding-distance margin; its conversion is a modelling choice
    that needs sensitivity analysis"): 'fixed' (D45) | 'gap' (HSRL's margin x the guaranteed gap L_x - U_y, in (0, 1])
    | 'gap_shuffled' (control: the same margins permuted among the term's certified tuples in the batch) |
    'similarity' (the gap on the plan's similarity scale t = 1 - d/4, i.e. a squared-distance margin of 4 x gap)."""
    needs_votes = True
    ORDERINGS = {1: ("ap", "an"), 2: ("ap", "nc"), 3: ("ap", "ac")}
    TERM_ROLES = {1: "apn", 2: "apnc", 3: "apc"}
    MARGINS = ("fixed", "gap", "gap_shuffled", "similarity")

    def __init__(self, alpha=1.0, beta=0.5, gamma=0.5, terms=(1, 2, 3), select="certified", margin="fixed"):
        super().__init__()
        if select not in ("certified", "random", "confidence"):
            raise ValueError(select)
        if margin not in self.MARGINS or (margin != "fixed" and select != "certified"):
            raise ValueError(f"margin={margin} with select={select}")
        self.alpha, self.beta, self.gamma, self.terms, self.select = alpha, beta, gamma, set(terms), select
        self.margin = margin

    def _margins(self, base, gap, cert, meta):
        if self.margin == "fixed":
            return base
        g = gap.clamp(min=0) * cert.float()
        if self.margin == "similarity":
            return 4.0 * g
        m = base * g
        if self.margin == "gap_shuffled":
            idx = cert.nonzero(as_tuple=True)[0]
            m = m.clone()
            m[idx] = m[idx][torch.randperm(len(idx), generator=meta["gen"]).to(idx.device)]
        return m

    def _keep(self, cert, k, meta):
        if self.select == "certified":
            return cert.float()
        keep, m = torch.zeros_like(cert, dtype=torch.float32), int(cert.sum())
        if m == 0:
            return keep
        noise = torch.rand(len(cert), generator=meta["gen"]).to(cert.device)
        if self.select == "random":
            score = noise
        else:   # most extreme votes first: mean |2q - 1| over the term's images, ties broken at random
            score = torch.stack([(2 * meta["q"][r] - 1).abs() for r in self.TERM_ROLES[k]]).mean(0) + 1e-6 * noise
        keep[score.topk(m).indices] = 1.0
        return keep

    def forward(self, z, tuples, meta):
        base = {1: self.alpha, 2: self.beta, 3: self.gamma}
        cert = {k: meta["L"][x] > meta["U"][y] + CERT_EPS for k, (x, y) in self.ORDERINGS.items()}
        marg = {k: self._margins(base[k], meta["L"][x] - meta["U"][y], cert[k], meta)
                for k, (x, y) in self.ORDERINGS.items()}
        log = hsrl_hinges(z, tuples, marg[1], marg[2], marg[3])
        per = torch.zeros_like(log["d_ap"])
        for k in self.ORDERINGS:
            keep = self._keep(cert[k], k, meta) if k in self.terms else torch.zeros_like(per)
            log[f"t{k}"] = log[f"t{k}"] * keep
            log[f"cert{k}"], log[f"kept{k}"] = cert[k].float(), keep
            if self.margin != "fixed":
                log[f"margin{k}"] = marg[k] * keep
            per = per + log[f"t{k}"]
        log["loss"] = per
        return per.mean(), {k: v.detach() for k, v in log.items()}


def pair_similarity(zi, zj):
    """t = 1 - d/4 in [0, 1] for L2-normalised embeddings (the plan's similarity scale)."""
    return 1.0 - sq_dist(zi, zj) / 4.0


class IntervalLoss(nn.Module):
    """Supervisor's plan §3 (pairwise bounds): penalise t only outside the feasible agreement interval [L, U]:
        max(0, L - t)^2 + max(0, t - U)^2.
    Pair-based: forward(z, pairs, meta) with pairs = {'i', 'j'} index tensors and meta = {'L', 'U'} per pair.
    With an exactly observed agreement (L = U = s) it is squared error to s."""

    def forward(self, z, pairs, meta):
        t = pair_similarity(z[pairs["i"]], z[pairs["j"]])
        per = F.relu(meta["L"] - t) ** 2 + F.relu(t - meta["U"]) ** 2
        return per.mean(), {"t": t.detach(), "loss": per.detach()}


class WorstCaseIntervalLoss(nn.Module):
    """Supervisor's plan §4 (independent worst-case pair loss): expected squared cost at agreement s,
        c(s, t) = s (t - 1)^2 + (1 - s) t^2,
    maximised over s in [L, U] for each pair separately. c is linear in s, so the maximum is at an endpoint.
    With L = U = s it is the expected cost at the observed agreement."""

    def forward(self, z, pairs, meta):
        t = pair_similarity(z[pairs["i"]], z[pairs["j"]])
        cost = lambda s: s * (t - 1) ** 2 + (1 - s) * t ** 2
        per = torch.maximum(cost(meta["L"]), cost(meta["U"]))
        return per.mean(), {"t": t.detach(), "loss": per.detach()}


class TuplePairLoss(nn.Module):
    """Stage I wrapper for a pair loss (interval or independent worst case): applied to the six pairs of every mined
    tuple, so tuple sampling stays HSRL's (plan §5). HSRL's hinges at the paper's margins are logged as diagnostics
    only; they are not trained."""
    needs_votes = True

    def __init__(self, pair_loss, alpha=1.0, beta=0.5, gamma=0.5):
        super().__init__()
        self.pair_loss, self.alpha, self.beta, self.gamma = pair_loss, alpha, beta, gamma

    def forward(self, z, tuples, meta):
        pairs = {"i": torch.cat([tuples[u] for u, _ in PAIR_ROLES.values()]),
                 "j": torch.cat([tuples[v] for _, v in PAIR_ROLES.values()])}
        bounds = {b: torch.cat([meta[b][p] for p in PAIR_ROLES]) for b in ("L", "U")}
        loss, lg = self.pair_loss(z, pairs, bounds)
        log = {k: v.detach() for k, v in hsrl_hinges(z, tuples, self.alpha, self.beta, self.gamma).items()}
        log["loss"] = lg["loss"].view(len(PAIR_ROLES), -1).mean(0)
        return loss, log


class JointFourImageLoss(nn.Module):
    """Supervisor's plan §4, joint four-image loss: L_joint = max_v (1/R) sum_b v(b) C(b), with
    C(b) = (1/6) sum_ij (t_ij - e_ij(b))^2, over reader allocations v consistent with the four images' vote counts.
    For fixed (detached) t the inner problem is linear in v; it is solved exactly (model='exact': integer v, common
    R-reader panel, MHIST) or as the LP relaxation (model='relax': fractional v, marginals q). The maximising
    agreements s* are held fixed and (1/6) sum_ij [t_ij^2 + s*_ij (1 - 2 t_ij)] is backpropagated, a subgradient of
    the finite maximum. Counts only: reader identities are not used. Mean over tuples."""
    needs_votes = True

    def __init__(self, alpha=1.0, beta=0.5, gamma=0.5, model="exact"):
        super().__init__()
        if model not in ("exact", "relax"):
            raise ValueError(model)
        self.alpha, self.beta, self.gamma, self.model = alpha, beta, gamma, model

    def forward(self, z, tuples, meta):
        t = torch.stack([pair_similarity(z[tuples[u]], z[tuples[v]]) for u, v in PAIR_ROLES.values()], 1)   # (T, 6)
        tn = t.detach().double().cpu().numpy()
        if self.model == "exact":
            m = np.stack([meta["k"][r] for r in "apnc"], 1)
            R = np.stack([meta["R"][r] for r in "apnc"], 1)
            if not (R == R[:, :1]).all():
                raise ValueError("exact joint loss needs a common reader panel (same number of readers per tuple)")
            s = np.stack([joint_agreements(tn[i], m[i], R[i, 0], True) for i in range(len(tn))])
        else:
            m = np.stack([meta["q"][r].cpu().numpy() for r in "apnc"], 1).astype(np.float64)
            s = np.stack([joint_agreements(tn[i], m[i], 1.0, False) for i in range(len(tn))])
        s = torch.as_tensor(s, dtype=t.dtype, device=t.device)
        per = (t ** 2 + s * (1 - 2 * t)).mean(1)
        log = {k: v.detach() for k, v in hsrl_hinges(z, tuples, self.alpha, self.beta, self.gamma).items()}
        log["loss"] = per.detach()
        return per.mean(), log


STRUCTURAL_LOSSES = {"hsrl": HSRLLoss, "interval": IntervalLoss, "interval_worstcase": WorstCaseIntervalLoss,
                     "supported": SupportedOrderingLoss, "joint": JointFourImageLoss}


def build_structural_loss(cfg):
    """Stage I loss from the stage1 config. Vote-aware losses (all but 'hsrl') read only labelled-set votes."""
    name = cfg.get("loss", "hsrl")
    margins = (cfg["alpha"], cfg["beta"], cfg["gamma"])
    if name == "hsrl":
        return HSRLLoss(*margins, cfg.get("terms", (1, 2, 3)))
    if name == "supported":
        return SupportedOrderingLoss(*margins, cfg.get("terms", (1, 2, 3)), cfg.get("select", "certified"),
                                     cfg.get("margin", "fixed"))
    if name in ("interval", "interval_worstcase"):
        return TuplePairLoss(STRUCTURAL_LOSSES[name](), *margins)
    if name == "joint":
        return JointFourImageLoss(*margins, cfg.get("joint_model", "exact"))
    raise KeyError(f"structural loss {name} not implemented; known: {sorted(STRUCTURAL_LOSSES)}")


def soft_cross_entropy(logits, target_probs):
    return -(target_probs * F.log_softmax(logits.float(), dim=1)).sum(1).mean()
