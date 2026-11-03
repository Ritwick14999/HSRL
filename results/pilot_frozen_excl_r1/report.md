# EXPLORATORY PILOT: interval losses on frozen ImageNet features

15 (fold, seed) pairs. Test = held-out slides, non-tie patches. Head methods are evaluated with a hard-target linear probe on the head embedding. Criterion fixed in advance: >= +1 point on balanced or split-vote accuracy over the best baseline in >= 12/15 pairs and on >= 2/3 folds.

## Mean ± std per method

| method | runs | bal acc | split-vote acc | unanimous acc | Brier | retrieval ρ |
|---|---|---|---|---|---|---|
| probe_hard | 15 | 0.707 ± 0.010 | 0.588 ± 0.028 | 0.735 ± 0.016 | 0.257 ± 0.008 | nan |
| probe_soft | 15 | 0.705 ± 0.009 | 0.590 ± 0.013 | 0.732 ± 0.011 | 0.252 ± 0.005 | nan |
| annotator_aware | 15 | 0.720 ± 0.024 | 0.605 ± 0.018 | 0.779 ± 0.023 | 0.180 ± 0.016 | nan |
| hsrl_t13 | 15 | 0.717 ± 0.023 | 0.597 ± 0.019 | 0.766 ± 0.026 | 0.241 ± 0.019 | 0.318 ± 0.046 |
| interval_linked | 15 | 0.728 ± 0.018 | 0.606 ± 0.018 | 0.776 ± 0.024 | 0.242 ± 0.019 | 0.335 ± 0.054 |
| interval_permuted | 15 | 0.730 ± 0.018 | 0.609 ± 0.022 | 0.777 ± 0.024 | 0.241 ± 0.020 | 0.337 ± 0.056 |
| interval_counts_only | 15 | 0.724 ± 0.020 | 0.602 ± 0.022 | 0.777 ± 0.023 | 0.243 ± 0.021 | 0.345 ± 0.059 |
| worstcase_linked | 15 | 0.729 ± 0.019 | 0.610 ± 0.020 | 0.777 ± 0.023 | 0.239 ± 0.018 | 0.337 ± 0.056 |
| worstcase_permuted | 15 | 0.730 ± 0.018 | 0.610 ± 0.021 | 0.777 ± 0.023 | 0.240 ± 0.020 | 0.339 ± 0.057 |
| worstcase_counts_only | 15 | 0.729 ± 0.020 | 0.610 ± 0.023 | 0.780 ± 0.023 | 0.236 ± 0.019 | 0.349 ± 0.057 |

Best baseline: balanced accuracy = `annotator_aware`, split-vote accuracy = `annotator_aware`.

## Paired differences vs the best baseline

| method | vs | metric | mean_diff | ci_lo | ci_hi | pairs_ge_1pt | pairs_better | n_pairs | folds_ge_1pt | per_fold |
|---|---|---|---|---|---|---|---|---|---|---|
| interval_linked | annotator_aware | bal acc | 0.008 | 0.001 | 0.014 | 7 | 10 | 15 | 1 | f0:+0.019 / f1:+0.005 / f2:-0.000 |
| interval_linked | annotator_aware | split-vote acc | 0.001 | -0.007 | 0.010 | 5 | 5 | 15 | 0 | f0:-0.002 / f1:+0.003 / f2:+0.003 |
| interval_linked | annotator_aware | unanimous acc | -0.003 | -0.008 | 0.003 | 1 | 5 | 15 | 0 | f0:+0.010 / f1:-0.007 / f2:-0.010 |
| interval_linked | annotator_aware | Brier | 0.062 | 0.057 | 0.067 | 0 | 0 | 15 | 0 | f0:+0.055 / f1:+0.058 / f2:+0.072 |
| interval_permuted | annotator_aware | bal acc | 0.010 | 0.004 | 0.016 | 8 | 11 | 15 | 1 | f0:+0.020 / f1:+0.006 / f2:+0.004 |
| interval_permuted | annotator_aware | split-vote acc | 0.004 | -0.006 | 0.014 | 4 | 6 | 15 | 0 | f0:-0.003 / f1:+0.007 / f2:+0.008 |
| interval_permuted | annotator_aware | unanimous acc | -0.002 | -0.007 | 0.004 | 3 | 5 | 15 | 1 | f0:+0.010 / f1:-0.006 / f2:-0.009 |
| interval_permuted | annotator_aware | Brier | 0.061 | 0.056 | 0.067 | 0 | 0 | 15 | 0 | f0:+0.055 / f1:+0.056 / f2:+0.073 |
| interval_counts_only | annotator_aware | bal acc | 0.004 | -0.002 | 0.009 | 4 | 9 | 15 | 1 | f0:+0.011 / f1:+0.003 / f2:-0.002 |
| interval_counts_only | annotator_aware | split-vote acc | -0.003 | -0.013 | 0.006 | 4 | 6 | 15 | 0 | f0:-0.011 / f1:+0.005 / f2:-0.004 |
| interval_counts_only | annotator_aware | unanimous acc | -0.002 | -0.006 | 0.003 | 1 | 7 | 15 | 0 | f0:+0.006 / f1:-0.005 / f2:-0.006 |
| interval_counts_only | annotator_aware | Brier | 0.063 | 0.058 | 0.067 | 0 | 0 | 15 | 0 | f0:+0.062 / f1:+0.055 / f2:+0.071 |
| worstcase_linked | annotator_aware | bal acc | 0.009 | 0.002 | 0.015 | 7 | 10 | 15 | 1 | f0:+0.020 / f1:+0.006 / f2:+0.000 |
| worstcase_linked | annotator_aware | split-vote acc | 0.005 | -0.003 | 0.013 | 5 | 7 | 15 | 0 | f0:-0.001 / f1:+0.009 / f2:+0.006 |
| worstcase_linked | annotator_aware | unanimous acc | -0.002 | -0.008 | 0.004 | 4 | 5 | 15 | 1 | f0:+0.012 / f1:-0.008 / f2:-0.009 |
| worstcase_linked | annotator_aware | Brier | 0.059 | 0.054 | 0.064 | 0 | 0 | 15 | 0 | f0:+0.052 / f1:+0.056 / f2:+0.070 |
| worstcase_permuted | annotator_aware | bal acc | 0.010 | 0.004 | 0.016 | 9 | 10 | 15 | 1 | f0:+0.020 / f1:+0.006 / f2:+0.005 |
| worstcase_permuted | annotator_aware | split-vote acc | 0.005 | -0.005 | 0.015 | 5 | 7 | 15 | 1 | f0:+0.000 / f1:+0.005 / f2:+0.011 |
| worstcase_permuted | annotator_aware | unanimous acc | -0.001 | -0.007 | 0.004 | 3 | 6 | 15 | 1 | f0:+0.011 / f1:-0.007 / f2:-0.007 |
| worstcase_permuted | annotator_aware | Brier | 0.059 | 0.055 | 0.064 | 0 | 0 | 15 | 0 | f0:+0.054 / f1:+0.054 / f2:+0.070 |
| worstcase_counts_only | annotator_aware | bal acc | 0.009 | 0.003 | 0.014 | 9 | 10 | 15 | 1 | f0:+0.016 / f1:+0.007 / f2:+0.003 |
| worstcase_counts_only | annotator_aware | split-vote acc | 0.005 | -0.004 | 0.015 | 5 | 7 | 15 | 1 | f0:-0.004 / f1:+0.007 / f2:+0.013 |
| worstcase_counts_only | annotator_aware | unanimous acc | 0.001 | -0.003 | 0.005 | 1 | 8 | 15 | 0 | f0:+0.009 / f1:-0.002 / f2:-0.003 |
| worstcase_counts_only | annotator_aware | Brier | 0.056 | 0.052 | 0.060 | 0 | 0 | 15 | 0 | f0:+0.054 / f1:+0.050 / f2:+0.063 |

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
| interval | -0.002 | -0.003 | 0 | 2 | 0 | 0 | False |
| worstcase | -0.002 | -0.000 | 0 | 2 | 0 | 0 | False |
