"""Pairwise reader-agreement targets for pair-based structural losses (labelled training patches only).

counts_only  L = |q_i + q_j - 1|, U = 1 - |q_i - q_j|   (Fréchet bounds; assume a common reader panel)
linked       s = fraction of shared readers (valid votes on both) giving the same class; pairs with
             >= min_shared shared readers get L = U = s, the rest fall back to the counts-only bounds
permuted     as linked, after votes are reassigned among each image's observed readers (hsrl/data/votes.py),
             which keeps q, reader membership and missingness but destroys cross-image correspondence
"""
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

VOTE_MODES = ("linked", "permuted", "counts_only")

# Four-image tuples (a, p, n, c), plan §4. One reader's decisions form a pattern b in {0,1}^4; e_ij(b) = 1 if the
# pattern gives images i and j the same class.
PAIR_ROLES = {"ap": ("a", "p"), "an": ("a", "n"), "ac": ("a", "c"), "pn": ("p", "n"), "pc": ("p", "c"), "nc": ("n", "c")}
PAIR_NAMES = list(PAIR_ROLES)
PAIRS = [("apnc".index(u), "apnc".index(v)) for u, v in PAIR_ROLES.values()]
PAT = np.array([[(b >> (3 - i)) & 1 for i in range(4)] for b in range(16)], dtype=float)   # (16, 4)
E = np.array([[float(PAT[b, i] == PAT[b, j]) for i, j in PAIRS] for b in range(16)])          # (16, 6)
A_MARG = np.vstack([np.ones(16), PAT.T])                                                        # (5, 16)


def counts_bounds(qi, qj):
    return np.abs(qi + qj - 1.0), 1.0 - np.abs(qi - qj)


def linked_agreement(V, i, j):
    """V: (N, R) int votes with -1 = no vote. Returns (s, n_shared) for the pairs (i, j)."""
    vi, vj = V[i], V[j]
    shared = (vi >= 0) & (vj >= 0)
    n = shared.sum(1)
    same = (shared & (vi == vj)).sum(1)
    s = np.where(n > 0, same / np.maximum(n, 1), np.nan)
    return s, n


def pair_bounds(V, q, i, j, mode, min_shared=3):
    """Agreement interval [L, U] per pair, plus the fraction of pairs whose agreement is pinned exactly."""
    L, U = counts_bounds(q[i], q[j])
    if mode == "counts_only":
        return L, U, 0.0
    if mode not in ("linked", "permuted"):
        raise ValueError(mode)
    s, n = linked_agreement(V, i, j)
    exact = n >= min_shared
    L, U = L.copy(), U.copy()
    L[exact] = s[exact]
    U[exact] = s[exact]
    return L, U, float(exact.mean())


def tuple_bounds(m, total):
    """Fréchet bounds of the six pair agreements of a tuple with SSA/G4 counts m out of `total` readers (common
    panel), in units of 1/total: integers for exact counts, fractions when m = q and total = 1."""
    L = np.array([abs(m[i] + m[j] - total) for i, j in PAIRS], float)
    U = np.array([total - abs(m[i] - m[j]) for i, j in PAIRS], float)
    return L, U


def solve_allocation(c, A, b, total, integer):
    """min c.x over reader allocations x >= 0 with A x = b: integer x (MILP) or the LP relaxation."""
    if integer:
        return milp(c, constraints=LinearConstraint(A, b, b), integrality=np.ones(len(c)), bounds=Bounds(0, total),
                    options={"mip_rel_gap": 0.0})
    return linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method="highs")


def joint_worst_case(w, m, total, integer):
    """max over reader allocations x (16 patterns, sum = total, column sums = m) of sum_ij w_ij s_ij, the inner
    maximisation of the plan's joint loss. Returns (value, s) with s the six agreements (fractions) of the maximiser."""
    b = np.concatenate([[total], m])
    r = solve_allocation(-(E @ w), A_MARG, b, total, integer)
    if r.status != 0 or r.x is None:
        raise RuntimeError(f"solver failed (status {r.status}) for marginals {m}")
    x = np.round(r.x) if integer else r.x
    if integer and not np.allclose(A_MARG @ x, b):
        raise RuntimeError(f"rounded integer allocation breaks the marginals {m}")
    s = E.T @ x / total
    return float(w @ s), s


def joint_agreements(t, m, total, integer):
    """Worst-case agreements s* (6,) of the plan's joint loss for similarities t (6,). With at most two split-vote
    images only one pair agreement is free, so the joint and independent worst cases coincide and no solver is needed
    (confirmed on every such tuple in results/joint_check)."""
    w = 1.0 - 2.0 * t
    if ((m > 0) & (m < total)).sum() <= 2:
        L, U = tuple_bounds(m, total)
        return np.where(w > 0, U, L) / total
    return joint_worst_case(w, m, total, integer)[1]
