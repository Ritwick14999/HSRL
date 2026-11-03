"""In-batch tuple mining for Stage I (not specified in the paper; see ASSUMPTIONS.md A2.x).

Every sample of a class-balanced labelled batch is an anchor a:
  p  a random same-class sample (p != a)
  n  the nearest different-class sample in embedding space (hard negative)
  c  conf_rule='second_nearest' (default): the second-nearest different-class sample
     conf_rule='boundary': the different-class sample (excluding n) with the smallest gap between its
       distances to its own class centroid and to the nearest other-class centroid (batch centroids)
Mining runs on detached embeddings; the loss is then computed on the gathered embeddings with gradient.
"""
import torch

CONF_RULES = ("second_nearest", "boundary")


@torch.no_grad()
def pairwise_sq_dist(z):
    sq = (z * z).sum(1)
    return (sq[:, None] + sq[None, :] - 2 * z @ z.T).clamp_min(0)


@torch.no_grad()
def mine_tuples(z, y, conf_rule="second_nearest", generator=None):
    if conf_rule not in CONF_RULES:
        raise ValueError(conf_rule)
    z = z.detach().float()
    B = z.shape[0]
    dev = z.device
    D = pairwise_sq_dist(z)
    same = y[:, None] == y[None, :]
    eye = torch.eye(B, dtype=torch.bool, device=dev)
    pos_cand = same & ~eye
    neg = ~same

    r = torch.rand(B, B, generator=generator).to(dev)
    r[~pos_cand] = -1.0
    p = r.argmax(1)

    Dn = D.masked_fill(~neg, float("inf"))
    order = Dn.argsort(1)
    n = order[:, 0]
    if conf_rule == "second_nearest":
        c = order[:, 1]
    else:
        classes = torch.unique(y)
        cent = torch.stack([z[y == k].mean(0) for k in classes])           # (K, D), not renormalised
        dc = ((z[:, None, :] - cent[None]) ** 2).sum(-1)                   # (B, K)
        own = (y[:, None] == classes[None]).float().argmax(1)
        d_own = dc.gather(1, own[:, None]).squeeze(1)
        d_other = dc.masked_fill(classes[None] == y[:, None], float("inf")).min(1).values
        gap = (d_own - d_other).abs()                                      # small = near the boundary
        cand = neg.clone()
        cand[torch.arange(B, device=dev), n] = False
        score = gap[None, :].expand(B, B).masked_fill(~cand, float("inf"))
        c = score.argmin(1)

    valid = pos_cand.any(1) & (neg.sum(1) >= 2)
    a = torch.arange(B, device=dev)[valid]
    return {"a": a, "p": p[valid], "n": n[valid], "c": c[valid]}
