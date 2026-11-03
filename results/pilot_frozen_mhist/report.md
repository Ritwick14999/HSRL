# EXPLORATORY PILOT: interval losses on frozen ImageNet features

15 (fold, seed) pairs. Test = held-out slides (Gleason) or the official test set (MHIST), non-tie patches. Head methods are evaluated with a hard-target linear probe on the head embedding. Criterion fixed in advance: >= +1 point on balanced or split-vote accuracy over the best baseline in >= 12/15 pairs and on >= 4/5 folds (MHIST: labelled draws).

## Mean ± std per method

| method | runs | bal acc | split-vote acc | unanimous acc | Brier |
|---|---|---|---|---|---|
| probe_hard | 15 | 0.721 ± 0.026 | 0.650 ± 0.029 | 0.794 ± 0.025 | 0.274 ± 0.024 |
| probe_soft | 15 | 0.695 ± 0.023 | 0.638 ± 0.026 | 0.784 ± 0.034 | 0.252 ± 0.023 |
| hsrl_t13 | 15 | 0.707 ± 0.039 | 0.696 ± 0.031 | 0.795 ± 0.040 | 0.246 ± 0.028 |
| interval_counts_only | 15 | 0.743 ± 0.021 | 0.720 ± 0.021 | 0.834 ± 0.022 | 0.218 ± 0.016 |
| worstcase_counts_only | 15 | 0.742 ± 0.025 | 0.712 ± 0.021 | 0.841 ± 0.027 | 0.221 ± 0.017 |

Best baseline: balanced accuracy = `probe_hard`, split-vote accuracy = `hsrl_t13`.

## Paired differences vs the best baseline

| method | vs | metric | mean_diff | ci_lo | ci_hi | pairs_ge_1pt | pairs_better | n_pairs | folds_ge_1pt | per_fold |
|---|---|---|---|---|---|---|---|---|---|---|
| interval_counts_only | probe_hard | bal acc | 0.022 | 0.014 | 0.030 | 12 | 13 | 15 | 4 | f0:+0.033 / f1:+0.023 / f2:+0.032 / f3:+0.025 / f4:-0.002 |
| interval_counts_only | hsrl_t13 | split-vote acc | 0.024 | 0.015 | 0.034 | 13 | 13 | 15 | 4 | f0:+0.029 / f1:+0.010 / f2:+0.014 / f3:+0.042 / f4:+0.028 |
| interval_counts_only | probe_hard | unanimous acc | 0.039 | 0.027 | 0.051 | 12 | 14 | 15 | 4 | f0:+0.056 / f1:+0.050 / f2:+0.045 / f3:+0.042 / f4:+0.003 |
| interval_counts_only | probe_hard | Brier | -0.056 | -0.064 | -0.049 | 15 | 15 | 15 | 5 | f0:-0.065 / f1:-0.060 / f2:-0.059 / f3:-0.065 / f4:-0.033 |
| worstcase_counts_only | probe_hard | bal acc | 0.021 | 0.010 | 0.032 | 12 | 13 | 15 | 4 | f0:+0.036 / f1:+0.024 / f2:+0.037 / f3:+0.018 / f4:-0.010 |
| worstcase_counts_only | hsrl_t13 | split-vote acc | 0.016 | 0.005 | 0.026 | 8 | 12 | 15 | 4 | f0:+0.028 / f1:-0.003 / f2:+0.013 / f3:+0.026 / f4:+0.013 |
| worstcase_counts_only | probe_hard | unanimous acc | 0.047 | 0.033 | 0.061 | 13 | 13 | 15 | 4 | f0:+0.063 / f1:+0.062 / f2:+0.059 / f3:+0.046 / f4:+0.005 |
| worstcase_counts_only | probe_hard | Brier | -0.053 | -0.062 | -0.045 | 15 | 15 | 15 | 5 | f0:-0.066 / f1:-0.057 / f2:-0.061 / f3:-0.057 / f4:-0.026 |

## Pre-registered success criterion

| method | bal acc criterion | split acc criterion | SUCCESS |
|---|---|---|---|
| interval_counts_only | True | True | True |
| worstcase_counts_only | True | False | True |

## Linkage test: linked − permuted (same standard)

-
