# EXPLORATORY PILOT: interval losses on frozen ImageNet features

15 (fold, seed) pairs. Test = held-out slides, non-tie patches. Head methods are evaluated with a hard-target linear probe on the head embedding. Criterion fixed in advance: >= +1 point on balanced or split-vote accuracy over the best baseline in >= 12/15 pairs and on >= 2/3 folds.

## Mean ± std per method

| method | runs | bal acc | split-vote acc | unanimous acc | Brier | retrieval ρ |
|---|---|---|---|---|---|---|
| probe_hard | 15 | 0.702 ± 0.003 | 0.626 ± 0.013 | 0.729 ± 0.009 | 0.267 ± 0.007 | nan |
| probe_soft | 15 | 0.671 ± 0.014 | 0.586 ± 0.027 | 0.717 ± 0.018 | 0.270 ± 0.021 | nan |
| annotator_aware | 15 | 0.720 ± 0.018 | 0.600 ± 0.026 | 0.807 ± 0.021 | 0.188 ± 0.015 | nan |
| hsrl_t13 | 15 | 0.713 ± 0.017 | 0.600 ± 0.028 | 0.784 ± 0.020 | 0.246 ± 0.019 | 0.297 ± 0.037 |
| interval_linked | 15 | 0.724 ± 0.015 | 0.601 ± 0.017 | 0.802 ± 0.025 | 0.241 ± 0.022 | 0.306 ± 0.045 |
| interval_permuted | 15 | 0.724 ± 0.017 | 0.603 ± 0.023 | 0.801 ± 0.027 | 0.242 ± 0.024 | 0.313 ± 0.049 |
| interval_counts_only | 15 | 0.718 ± 0.020 | 0.593 ± 0.028 | 0.807 ± 0.027 | 0.239 ± 0.025 | 0.329 ± 0.053 |
| worstcase_linked | 15 | 0.725 ± 0.016 | 0.603 ± 0.018 | 0.801 ± 0.026 | 0.239 ± 0.022 | 0.315 ± 0.047 |
| worstcase_permuted | 15 | 0.726 ± 0.018 | 0.606 ± 0.023 | 0.801 ± 0.027 | 0.240 ± 0.024 | 0.321 ± 0.049 |
| worstcase_counts_only | 15 | 0.723 ± 0.015 | 0.605 ± 0.023 | 0.802 ± 0.026 | 0.236 ± 0.023 | 0.331 ± 0.050 |

Best baseline: balanced accuracy = `annotator_aware`, split-vote accuracy = `probe_hard`.

## Paired differences vs the best baseline

| method | vs | metric | mean_diff | ci_lo | ci_hi | pairs_ge_1pt | pairs_better | n_pairs | folds_ge_1pt | per_fold |
|---|---|---|---|---|---|---|---|---|---|---|
| interval_linked | annotator_aware | bal acc | 0.004 | 0.000 | 0.007 | 2 | 12 | 15 | 0 | f0:+0.007 / f1:-0.001 / f2:+0.006 |
| interval_linked | probe_hard | split-vote acc | -0.025 | -0.029 | -0.020 | 0 | 0 | 15 | 0 | f0:-0.029 / f1:-0.015 / f2:-0.030 |
| interval_linked | annotator_aware | unanimous acc | -0.005 | -0.009 | -0.002 | 0 | 2 | 15 | 0 | f0:+0.000 / f1:-0.006 / f2:-0.011 |
| interval_linked | annotator_aware | Brier | 0.053 | 0.048 | 0.058 | 0 | 0 | 15 | 0 | f0:+0.046 / f1:+0.048 / f2:+0.064 |
| interval_permuted | annotator_aware | bal acc | 0.004 | 0.001 | 0.008 | 3 | 11 | 15 | 0 | f0:+0.010 / f1:+0.001 / f2:+0.002 |
| interval_permuted | probe_hard | split-vote acc | -0.023 | -0.031 | -0.015 | 0 | 1 | 15 | 0 | f0:-0.027 / f1:-0.006 / f2:-0.035 |
| interval_permuted | annotator_aware | unanimous acc | -0.006 | -0.011 | -0.001 | 0 | 4 | 15 | 0 | f0:+0.002 / f1:-0.006 / f2:-0.015 |
| interval_permuted | annotator_aware | Brier | 0.054 | 0.048 | 0.060 | 0 | 0 | 15 | 0 | f0:+0.046 / f1:+0.048 / f2:+0.068 |
| interval_counts_only | annotator_aware | bal acc | -0.002 | -0.006 | 0.001 | 1 | 6 | 15 | 0 | f0:+0.002 / f1:-0.001 / f2:-0.007 |
| interval_counts_only | probe_hard | split-vote acc | -0.033 | -0.043 | -0.022 | 0 | 0 | 15 | 0 | f0:-0.032 / f1:-0.012 / f2:-0.053 |
| interval_counts_only | annotator_aware | unanimous acc | -0.000 | -0.005 | 0.004 | 1 | 8 | 15 | 0 | f0:+0.004 / f1:+0.004 / f2:-0.008 |
| interval_counts_only | annotator_aware | Brier | 0.050 | 0.044 | 0.057 | 0 | 0 | 15 | 0 | f0:+0.043 / f1:+0.042 / f2:+0.066 |
| worstcase_linked | annotator_aware | bal acc | 0.005 | 0.002 | 0.008 | 2 | 13 | 15 | 0 | f0:+0.007 / f1:+0.001 / f2:+0.005 |
| worstcase_linked | probe_hard | split-vote acc | -0.023 | -0.028 | -0.018 | 0 | 0 | 15 | 0 | f0:-0.026 / f1:-0.013 / f2:-0.030 |
| worstcase_linked | annotator_aware | unanimous acc | -0.006 | -0.010 | -0.002 | 0 | 3 | 15 | 0 | f0:-0.001 / f1:-0.004 / f2:-0.013 |
| worstcase_linked | annotator_aware | Brier | 0.051 | 0.046 | 0.056 | 0 | 0 | 15 | 0 | f0:+0.045 / f1:+0.046 / f2:+0.062 |
| worstcase_permuted | annotator_aware | bal acc | 0.006 | 0.003 | 0.009 | 2 | 11 | 15 | 0 | f0:+0.009 / f1:+0.004 / f2:+0.004 |
| worstcase_permuted | probe_hard | split-vote acc | -0.019 | -0.028 | -0.011 | 1 | 1 | 15 | 0 | f0:-0.024 / f1:-0.002 / f2:-0.031 |
| worstcase_permuted | annotator_aware | unanimous acc | -0.006 | -0.011 | -0.001 | 0 | 4 | 15 | 0 | f0:+0.001 / f1:-0.004 / f2:-0.014 |
| worstcase_permuted | annotator_aware | Brier | 0.051 | 0.046 | 0.057 | 0 | 0 | 15 | 0 | f0:+0.045 / f1:+0.045 / f2:+0.065 |
| worstcase_counts_only | annotator_aware | bal acc | 0.003 | 0.000 | 0.006 | 1 | 12 | 15 | 0 | f0:+0.007 / f1:-0.001 / f2:+0.004 |
| worstcase_counts_only | probe_hard | split-vote acc | -0.021 | -0.029 | -0.012 | 0 | 1 | 15 | 0 | f0:-0.023 / f1:-0.005 / f2:-0.033 |
| worstcase_counts_only | annotator_aware | unanimous acc | -0.005 | -0.009 | -0.001 | 0 | 5 | 15 | 0 | f0:+0.002 / f1:-0.005 / f2:-0.011 |
| worstcase_counts_only | annotator_aware | Brier | 0.048 | 0.043 | 0.053 | 0 | 0 | 15 | 0 | f0:+0.041 / f1:+0.043 / f2:+0.060 |

## Pre-registered success criterion

| method | bal acc criterion | split acc criterion | SUCCESS |
|---|---|---|---|
| interval_linked | False | False | False |
| interval_permuted | False | False | False |
| interval_counts_only | False | False | False |
| worstcase_linked | False | False | False |
| worstcase_permuted | False | False | False |
| worstcase_counts_only | False | False | False |

## Linkage test: linked − permuted (same standard)

| variant | bal acc: Δ | split-vote acc: Δ | bal acc: pairs ≥ +1pt | split-vote acc: pairs ≥ +1pt | bal acc: folds ≥ +1pt | split-vote acc: folds ≥ +1pt | LINKAGE MATTERS |
|---|---|---|---|---|---|---|---|
| interval | -0.001 | -0.002 | 0 | 1 | 0 | 0 | False |
| worstcase | -0.001 | -0.004 | 0 | 0 | 0 | 0 | False |
