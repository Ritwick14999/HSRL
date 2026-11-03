# EXPLORATORY PILOT: interval losses on fine-tuned features (supervised 10% backbone of each draw)

15 (fold, seed) pairs. Test = held-out slides (Gleason) or the official test set (MHIST), non-tie patches. Head methods are evaluated with a hard-target linear probe on the head embedding. Criterion fixed in advance: >= +1 point on balanced or split-vote accuracy over the best baseline in >= 12/15 pairs and on >= 4/5 folds (MHIST: labelled draws).

## Mean ± std per method

| method | runs | bal acc | split-vote acc | unanimous acc | Brier |
|---|---|---|---|---|---|
| probe_hard | 15 | 0.756 ± 0.033 | 0.670 ± 0.038 | 0.861 ± 0.041 | 0.261 ± 0.038 |
| probe_soft | 15 | 0.703 ± 0.022 | 0.634 ± 0.030 | 0.820 ± 0.023 | 0.233 ± 0.020 |
| hsrl_t13 | 15 | 0.760 ± 0.032 | 0.686 ± 0.040 | 0.865 ± 0.035 | 0.248 ± 0.036 |
| interval_counts_only | 15 | 0.759 ± 0.029 | 0.691 ± 0.036 | 0.868 ± 0.027 | 0.226 ± 0.030 |
| worstcase_counts_only | 15 | 0.765 ± 0.025 | 0.701 ± 0.033 | 0.878 ± 0.027 | 0.220 ± 0.029 |

Best baseline: balanced accuracy = `hsrl_t13`, split-vote accuracy = `hsrl_t13`.

## Paired differences vs the best baseline

| method | vs | metric | mean_diff | ci_lo | ci_hi | pairs_ge_1pt | pairs_better | n_pairs | folds_ge_1pt | per_fold |
|---|---|---|---|---|---|---|---|---|---|---|
| interval_counts_only | hsrl_t13 | bal acc | -0.001 | -0.006 | 0.005 | 1 | 8 | 15 | 0 | f0:+0.001 / f1:-0.002 / f2:+0.006 / f3:+0.008 / f4:-0.016 |
| interval_counts_only | hsrl_t13 | split-vote acc | 0.005 | 0.000 | 0.010 | 3 | 12 | 15 | 1 | f0:-0.003 / f1:+0.009 / f2:+0.006 / f3:+0.014 / f4:-0.001 |
| interval_counts_only | hsrl_t13 | unanimous acc | 0.003 | -0.005 | 0.011 | 6 | 9 | 15 | 2 | f0:+0.003 / f1:-0.002 / f2:+0.017 / f3:+0.017 / f4:-0.018 |
| interval_counts_only | hsrl_t13 | Brier | -0.021 | -0.026 | -0.017 | 15 | 15 | 15 | 5 | f0:-0.017 / f1:-0.017 / f2:-0.022 / f3:-0.035 / f4:-0.018 |
| worstcase_counts_only | hsrl_t13 | bal acc | 0.005 | -0.003 | 0.013 | 6 | 10 | 15 | 2 | f0:+0.007 / f1:-0.005 / f2:+0.019 / f3:+0.017 / f4:-0.013 |
| worstcase_counts_only | hsrl_t13 | split-vote acc | 0.015 | 0.009 | 0.021 | 11 | 14 | 15 | 4 | f0:+0.015 / f1:+0.015 / f2:+0.018 / f3:+0.028 / f4:-0.002 |
| worstcase_counts_only | hsrl_t13 | unanimous acc | 0.014 | 0.003 | 0.024 | 8 | 12 | 15 | 3 | f0:+0.022 / f1:+0.002 / f2:+0.041 / f3:+0.012 / f4:-0.008 |
| worstcase_counts_only | hsrl_t13 | Brier | -0.028 | -0.033 | -0.022 | 14 | 15 | 15 | 5 | f0:-0.035 / f1:-0.019 / f2:-0.034 / f3:-0.036 / f4:-0.015 |

## Pre-registered success criterion

| method | bal acc criterion | split acc criterion | SUCCESS |
|---|---|---|---|
| interval_counts_only | False | False | False |
| worstcase_counts_only | False | False | False |

## Linkage test: linked − permuted (same standard)

-
