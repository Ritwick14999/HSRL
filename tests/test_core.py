import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import pytest
import torch
import torch.nn.functional as F

from hsrl.losses import HSRLLoss
from hsrl.mining import mine_tuples, pairwise_sq_dist
from hsrl.samplers import ClassBalancedBatchSampler
from hsrl.data.votes import apply_vote_mode


def test_hsrl_loss_matches_worked_example():
    # slide notes: d_ap=0.3, d_an=0.8, d_nc=0.6, d_ac=0.7 -> hinges 0.5, 0.2, 0.1, total 0.8
    # realise these distances with explicit points: only the distances matter
    loss = HSRLLoss(1.0, 0.5, 0.5)
    d = {"d_ap": torch.tensor([0.3]), "d_an": torch.tensor([0.8]), "d_nc": torch.tensor([0.6]), "d_ac": torch.tensor([0.7])}
    t1 = F.relu(d["d_ap"] - d["d_an"] + 1.0)
    t2 = F.relu(d["d_ap"] - d["d_nc"] + 0.5)
    t3 = F.relu(d["d_ap"] - d["d_ac"] + 0.5)
    assert torch.allclose(torch.stack([t1, t2, t3]).squeeze(), torch.tensor([0.5, 0.2, 0.1]))
    # and through the module with 1-D points (squared distances are squares of gaps)
    a, p = 0.0, 0.3 ** 0.5
    n = 0.8 ** 0.5
    c = -(0.7 ** 0.5)          # d_ac = 0.7; d_nc = (n - c)^2 is then fixed
    z = torch.tensor([[a], [p], [n], [c]])
    tup = {k: torch.tensor([i]) for i, k in enumerate("apnc")}
    val, lg = loss(z, tup)
    d_nc = (n - c) ** 2
    expect = 0.5 + max(0, 0.3 - d_nc + 0.5) + 0.1
    assert abs(val.item() - expect) < 1e-5
    assert abs(lg["d_ap"].item() - 0.3) < 1e-5 and abs(lg["d_ac"].item() - 0.7) < 1e-5


def test_term_ablation_removes_beta_term():
    z = F.normalize(torch.randn(4, 8), dim=1)
    tup = {k: torch.tensor([i]) for i, k in enumerate("apnc")}
    full, lg = HSRLLoss(terms=(1, 2, 3))(z, tup)
    no2, _ = HSRLLoss(terms=(1, 3))(z, tup)
    assert torch.allclose(full - no2, lg["t2"].mean())


@pytest.mark.parametrize("rule", ["second_nearest", "boundary"])
def test_mining_roles(rule):
    torch.manual_seed(0)
    z = F.normalize(torch.randn(16, 8), dim=1)
    y = torch.tensor([0] * 8 + [1] * 8)
    t = mine_tuples(z, y, rule, torch.Generator().manual_seed(0))
    D = pairwise_sq_dist(z)
    assert len(t["a"]) == 16
    for a, p, n, c in zip(*(t[k].tolist() for k in "apnc")):
        assert y[p] == y[a] and p != a
        assert y[n] != y[a] and y[c] != y[a] and n != c
        negs = [j for j in range(16) if y[j] != y[a]]
        dn = sorted(negs, key=lambda j: D[a, j].item())
        assert n == dn[0]
        if rule == "second_nearest":
            assert c == dn[1]


def test_class_balanced_sampler():
    labels = np.array([0] * 30 + [1] * 70)
    s = ClassBalancedBatchSampler(labels, 16, seed=0)
    batches = list(s)
    assert len(batches) == 7
    for b in batches:
        assert len(b) == 16 and (labels[b] == 0).sum() == 8


def test_vote_modes_preserve_counts():
    cols = [f"r{k}" for k in range(1, 7)]
    df = pd.DataFrame({c: pd.array(v, dtype="Int64") for c, v in zip(cols, [[1, 0], [0, None], [1, 1], [None, 0], [1, 1], [None, None]])})
    perm = apply_vote_mode(df, cols, "permuted", seed=3)
    assert (perm[cols].notna().to_numpy() == df[cols].notna().to_numpy()).all()       # same readers observed
    assert (perm[cols].sum(axis=1) == df[cols].sum(axis=1)).all()                          # same counts
    assert apply_vote_mode(df, cols, "counts_only", 0)[cols].isna().all().all()
    assert apply_vote_mode(df, cols, "linked", 0).equals(df)


@pytest.mark.skipif(not (ROOT / "data/processed/gleason/p512/labels_benign-drop").exists(), reason="dataset not built")
def test_gleason_split_has_votes_only_on_labelled():
    from hsrl.data import load_dataset
    d = load_dataset({"dataset": "gleason", "processed_root": str(ROOT / "data/processed/gleason"), "tile_size": 512,
                      "benign_rule": "drop", "exclude_readers": [], "fold": 0})
    vote_like = {"r1", "r2", "r3", "r4", "r5", "r6", "q", "label", "majority_label", "votes_g4", "tie"}
    for name in ("unlabelled", "val", "test"):
        assert not (set(getattr(d, name).columns) & vote_like), name
    assert {"label", "q"} <= set(d.labelled.columns) and (d.labelled.label >= 0).all()
    ids = [set(getattr(d, n).patch_id) for n in ("labelled", "unlabelled", "val", "test")]
    assert all(not (a & b) for i, a in enumerate(ids) for b in ids[i + 1:])
    cores = [set(getattr(d, n).core_id) for n in ("labelled", "val", "test")]
    assert not (cores[1] & cores[2]) and not (cores[0] & cores[2]) and not (cores[0] & cores[1])


def _supported_inputs(T=40, seed=0):
    g = torch.Generator().manual_seed(seed)
    z = F.normalize(torch.randn(4 * T, 8, generator=g), dim=1)
    tuples = {r: torch.arange(i * T, (i + 1) * T) for i, r in enumerate("apnc")}
    L = {p: (torch.randint(0, 8, (T,), generator=g) / 7.0) for p in ("ap", "an", "ac", "pn", "pc", "nc")}
    U = {p: torch.clamp(L[p] + torch.randint(0, 4, (T,), generator=g) / 7.0, max=1.0) for p in L}
    q = {r: torch.rand(T, generator=g) for r in "apnc"}
    return z, tuples, {"L": L, "U": U, "q": q, "gen": torch.Generator().manual_seed(1)}


def test_supported_ordering_margin_modes():
    from hsrl.losses import SupportedOrderingLoss, hsrl_hinges
    z, tuples, meta = _supported_inputs()
    ref = hsrl_hinges(z, tuples, 1.0, 0.5, 0.5)
    orderings, base = {1: ("ap", "an"), 2: ("ap", "nc"), 3: ("ap", "ac")}, {1: 1.0, 2: 0.5, 3: 0.5}
    d_y = {1: ref["d_an"], 2: ref["d_nc"], 3: ref["d_ac"]}
    # fixed margins (D45): HSRL's hinges, kept where certified
    _, lg = SupportedOrderingLoss(margin="fixed")(z, tuples, meta)
    for k, (x, y) in orderings.items():
        cert = (meta["L"][x] > meta["U"][y] + 1e-6).float()
        assert cert.sum() > 0
        assert torch.allclose(lg[f"t{k}"], ref[f"t{k}"] * cert)
    # gap margins: HSRL's margin x guaranteed gap on certified hinges; similarity: 4 x gap
    for mode, scale in (("gap", base), ("similarity", {1: 4.0, 2: 4.0, 3: 4.0})):
        _, lg = SupportedOrderingLoss(margin=mode)(z, tuples, meta)
        for k, (x, y) in orderings.items():
            cert = (meta["L"][x] > meta["U"][y] + 1e-6).float()
            m = scale[k] * (meta["L"][x] - meta["U"][y]).clamp(min=0) * cert
            assert torch.allclose(lg[f"t{k}"], F.relu(ref["d_ap"] - d_y[k] + m) * cert, atol=1e-6)
            assert torch.allclose(lg[f"margin{k}"], m)
    # shuffled control: same kept hinges, same multiset of margins
    _, lg_g = SupportedOrderingLoss(margin="gap")(z, tuples, meta)
    _, lg_s = SupportedOrderingLoss(margin="gap_shuffled")(z, tuples, meta)
    for k in orderings:
        assert torch.equal(lg_g[f"kept{k}"], lg_s[f"kept{k}"])
        assert torch.allclose(lg_g[f"margin{k}"].sort().values, lg_s[f"margin{k}"].sort().values)
    with pytest.raises(ValueError):
        SupportedOrderingLoss(select="random", margin="gap")
