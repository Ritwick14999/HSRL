# EXPLORATORY PILOT: interval losses on frozen ImageNet features

1 (fold, seed) pairs. Test = held-out slides (Gleason) or the official test set (MHIST), non-tie patches. Head methods are evaluated with a hard-target linear probe on the head embedding. Criterion fixed in advance: >= +1 point on balanced or split-vote accuracy over the best baseline in >= 12/1 pairs and on >= 4/1 folds (MHIST: labelled draws).

## Mean ± std per method

| method | runs | bal acc | split-vote acc | unanimous acc | Brier |
|---|---|---|---|---|---|
| probe_hard | 1 | 0.700 | 0.619 | 0.765 | 0.301 |
| probe_soft | 1 | 0.666 | 0.602 | 0.737 | 0.280 |
| hsrl_t13 | 1 | 0.662 | 0.659 | 0.768 | 0.277 |
| interval_counts_only | 1 | 0.726 | 0.686 | 0.811 | 0.244 |
| worstcase_counts_only | 1 | 0.745 | 0.699 | 0.836 | 0.235 |

Best baseline: balanced accuracy = `probe_hard`, split-vote accuracy = `hsrl_t13`.

## Paired differences vs the best baseline

| method | vs | metric | mean_diff | ci_lo | ci_hi | pairs_ge_1pt | pairs_better | n_pairs | folds_ge_1pt | per_fold |
|---|---|---|---|---|---|---|---|---|---|---|
| interval_counts_only | probe_hard | bal acc | 0.026 | nan | nan | 1 | 1 | 1 | 1 | f0:+0.026 |
| interval_counts_only | hsrl_t13 | split-vote acc | 0.028 | nan | nan | 1 | 1 | 1 | 1 | f0:+0.027 |
| interval_counts_only | probe_hard | unanimous acc | 0.046 | nan | nan | 1 | 1 | 1 | 1 | f0:+0.046 |
| interval_counts_only | probe_hard | Brier | -0.057 | nan | nan | 1 | 1 | 1 | 1 | f0:-0.057 |
| worstcase_counts_only | probe_hard | bal acc | 0.045 | nan | nan | 1 | 1 | 1 | 1 | f0:+0.045 |
| worstcase_counts_only | hsrl_t13 | split-vote acc | 0.040 | nan | nan | 1 | 1 | 1 | 1 | f0:+0.040 |
| worstcase_counts_only | probe_hard | unanimous acc | 0.071 | nan | nan | 1 | 1 | 1 | 1 | f0:+0.071 |
| worstcase_counts_only | probe_hard | Brier | -0.066 | nan | nan | 1 | 1 | 1 | 1 | f0:-0.066 |

## Pre-registered success criterion

| method | bal acc criterion | split acc criterion | SUCCESS |
|---|---|---|---|
| interval_counts_only | False | False | False |
| worstcase_counts_only | False | False | False |

## Linkage test: linked − permuted (same standard)

-
