import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import torch
import torch.nn.functional as F

from hsrl.agreement import counts_bounds, linked_agreement, pair_bounds
from hsrl.losses import IntervalLoss, WorstCaseIntervalLoss, pair_similarity


def test_counts_bounds_plan_examples():
    # plan §3: q = 4/7 and 4/7 -> [1/7, 1]; 6/7 and 1 -> exactly 6/7; 6/7 and 0 -> exactly 1/7
    L, U = counts_bounds(np.array([4 / 7, 6 / 7, 6 / 7]), np.array([4 / 7, 1.0, 0.0]))
    assert np.allclose(L, [1 / 7, 6 / 7, 1 / 7]) and np.allclose(U, [1.0, 6 / 7, 1 / 7])


def test_linked_agreement_and_fallback():
    V = np.array([[1, 1, 0, -1], [1, 0, 0, 1], [-1, -1, 1, 1]])
    s, n = linked_agreement(V, np.array([0, 0]), np.array([1, 2]))
    assert n.tolist() == [3, 1] and np.isclose(s[0], 2 / 3)
    q = np.array([2 / 3, 2 / 4, 1.0])
    L, U, frac = pair_bounds(V, q, np.array([0, 0]), np.array([1, 2]), "linked", min_shared=3)
    assert np.isclose(L[0], 2 / 3) and np.isclose(U[0], 2 / 3)                   # exact, 3 shared readers
    L2, U2 = counts_bounds(q[[0]], q[[2]])
    assert np.isclose(L[1], L2[0]) and np.isclose(U[1], U2[0]) and frac == 0.5    # 1 shared -> counts fallback
    Lc, Uc, f0 = pair_bounds(V, q, np.array([0]), np.array([1]), "counts_only")
    assert f0 == 0.0 and Lc[0] <= 2 / 3 <= Uc[0]


def test_interval_loss_zero_inside_and_squared_outside():
    z = F.normalize(torch.tensor([[1.0, 0.0], [0.0, 1.0]]), dim=1)               # d = 2 -> t = 0.5
    pairs = {"i": torch.tensor([0]), "j": torch.tensor([1])}
    assert pair_similarity(z[[0]], z[[1]]).item() == 0.5
    inside, _ = IntervalLoss()(z, pairs, {"L": torch.tensor([0.4]), "U": torch.tensor([0.6])})
    below, _ = IntervalLoss()(z, pairs, {"L": torch.tensor([0.8]), "U": torch.tensor([0.9])})
    assert inside.item() == 0.0 and abs(below.item() - 0.09) < 1e-6


def test_worstcase_is_max_over_interval_endpoints():
    z = F.normalize(torch.tensor([[1.0, 0.0], [0.0, 1.0]]), dim=1)               # t = 0.5
    pairs = {"i": torch.tensor([0]), "j": torch.tensor([1])}
    t = 0.5
    cost = lambda s: s * (t - 1) ** 2 + (1 - s) * t ** 2
    val, _ = WorstCaseIntervalLoss()(z, pairs, {"L": torch.tensor([0.2]), "U": torch.tensor([0.9])})
    grid = max(cost(s) for s in np.linspace(0.2, 0.9, 71))
    assert abs(val.item() - grid) < 1e-6
