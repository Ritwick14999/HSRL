"""Vote-handling modes, applied ONLY to the labelled training table.

linked       reader identities kept as recorded (default)
permuted     within each image, the observed votes are randomly reassigned among that image's observed
             readers: per-image counts, reader membership and missingness are preserved, cross-image
             reader correspondence is destroyed
counts_only  reader identities removed; only votes_g4 / n_readers / q remain
"""
import numpy as np
import pandas as pd

VOTE_MODES = ("linked", "permuted", "counts_only")


def apply_vote_mode(df, reader_cols, mode, seed=0):
    if mode not in VOTE_MODES:
        raise ValueError(f"vote_mode {mode}; expected one of {VOTE_MODES}")
    out = df.copy()
    if mode == "linked":
        return out
    if mode == "counts_only":
        out[reader_cols] = pd.NA
        return out
    rng = np.random.default_rng(seed)
    v = out[reader_cols].to_numpy(dtype=object)
    for i in range(len(v)):
        obs = np.flatnonzero(pd.notna(v[i]))
        v[i, obs] = v[i, rng.permutation(obs)]
    for j, c in enumerate(reader_cols):
        out[c] = pd.array(v[:, j], dtype="Int64")
    return out
