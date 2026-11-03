"""Brute-force checks of the propositions in the proofs doc (vote bounds, supported-ordering certificate, worst-case
pair cost, joint vs pairwise worst case, LP relaxation). Common-panel model: R readers label every image.

Usage: python -I analysis/proof_checks.py
"""
import itertools
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hsrl.agreement import A_MARG, joint_worst_case, solve_allocation  # noqa: E402

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
L = lambda qi, qj: abs(qi + qj - 1)
U = lambda qi, qj: 1 - abs(qi - qj)


def vecs(R, k):
    return [np.array([1 if i in c else 0 for i in range(R)]) for c in itertools.combinations(range(R), k)]


def agree(u, v):
    return F(int((u == v).sum()), len(u))


def prop1(rmax=7):
    """Agreements reachable from counts = {L, L + 2/R, ..., U}."""
    bad = 0
    for R in range(1, rmax + 1):
        for ki, kj in itertools.product(range(R + 1), repeat=2):
            qi, qj = F(ki, R), F(kj, R)
            got = sorted({agree(vecs(R, ki)[0], b) for b in vecs(R, kj)})
            exp = [L(qi, qj) + F(2 * m, R) for m in range(int((U(qi, qj) - L(qi, qj)) * R / 2) + 1)]
            bad += got != exp
    return bad


def prop2(rmax=5):
    """min over allocations of s_x - s_y equals L_x - U_y (term 1: ap vs an; term 2: ap vs nc)."""
    bad = 0
    for R in range(1, rmax + 1):
        for k in itertools.product(range(R + 1), repeat=4):
            q = [F(x, R) for x in k]
            A = vecs(R, k[0])[0]
            P, N, C = vecs(R, k[1]), vecs(R, k[2]), vecs(R, k[3])
            bad += min(agree(A, p) - agree(A, n) for p in P for n in N) != L(q[0], q[1]) - U(q[0], q[2])
            bad += min(agree(A, p) - agree(n, c) for p in P for n in N for c in C) != L(q[0], q[1]) - U(q[2], q[3])
    return bad


def prop3():
    """argmin_t max_{s in [L, U]} c(s, t) = clip(1/2, L, U), on a grid of intervals."""
    ts, worst = np.linspace(0, 1, 20001), 0.0
    for Lv, Uv in itertools.combinations_with_replacement(np.linspace(0, 1, 21), 2):
        f = np.maximum(Lv * (ts - 1) ** 2 + (1 - Lv) * ts ** 2, Uv * (ts - 1) ** 2 + (1 - Uv) * ts ** 2)
        worst = max(worst, abs(ts[f.argmin()] - min(max(0.5, Lv), Uv)))
    return worst


def prop4(rmax=5, seed=0):
    """J <= I always; J = I with <= 2 split-vote images; how often J < I with 3 or 4."""
    rng, cnt = np.random.default_rng(seed), {"le2": [0, 0], "3plus": [0, 0], "J>I": 0}
    for R in range(2, rmax + 1):
        for k in itertools.product(range(R + 1), repeat=4):
            q = [F(x, R) for x in k]
            V = [vecs(R, k[0])[:1]] + [vecs(R, x) for x in k[1:]]
            key = "le2" if sum(0 < x < R for x in k) <= 2 else "3plus"
            for _ in range(3):
                t = rng.random(6)
                w = 1 - 2 * t
                ind = sum(t[i] ** 2 + float(U(q[a], q[b]) if w[i] > 0 else L(q[a], q[b])) * w[i] for i, (a, b) in enumerate(PAIRS))
                joint = max(sum(t[i] ** 2 + float(agree(v[a], v[b])) * w[i] for i, (a, b) in enumerate(PAIRS))
                            for v in itertools.product(*V))
                cnt["J>I"] += joint > ind + 1e-9
                cnt[key][0] += 1
                cnt[key][1] += ind - joint > 1e-9
    return cnt


def lp_checks(rmax=7):
    """|det| of all maximal minors of the allocation matrix, and LP vs exact integer optimum for the joint loss's
    objective (pairwise agreements only) and for arbitrary objectives over the 16 patterns."""
    dets = sorted({int(round(abs(np.linalg.det(A_MARG[:, list(c)])))) for c in itertools.combinations(range(16), 5)})
    r1, r2, pair, gen = np.random.default_rng(1), np.random.default_rng(2), [0, 0], [0, 0]
    for R in range(2, rmax + 1):
        for k in itertools.product(range(R + 1), repeat=4):
            if sum(0 < x < R for x in k) < 3:
                continue
            m, b = np.array(k, float), np.concatenate([[R], k]).astype(float)
            for _ in range(4):
                w = r1.uniform(-1, 1, 6)
                pair[0] += 1
                pair[1] += joint_worst_case(w, m, R, False)[0] - joint_worst_case(w, m, R, True)[0] > 1e-7
            for _ in range(3):
                c = r2.uniform(-1, 1, 16)
                gen[0] += 1
                gen[1] += c @ solve_allocation(c, A_MARG, b, R, True).x - c @ solve_allocation(c, A_MARG, b, R, False).x > 1e-7
    return dets, pair, gen


if __name__ == "__main__":
    print("Prop 1, R <= 7: violations", prop1())
    print("Prop 2, R <= 5: violations", prop2())
    print("Prop 3: max |argmin - clip(1/2, L, U)| on the grid", prop3())
    c = prop4()
    print(f"Prop 4, R <= 5: J > I in {c['J>I']} cases; <= 2 split-vote: J < I in {c['le2'][1]} of {c['le2'][0]}; "
          f"3-4 split-vote: J < I in {c['3plus'][1]} of {c['3plus'][0]}")
    dets, pair, gen = lp_checks()
    print("LP: |det| of 5x5 minors", dets, f"; joint-loss objective: LP > exact in {pair[1]} of {pair[0]}; "
          f"arbitrary objectives: LP better than exact in {gen[1]} of {gen[0]}")
