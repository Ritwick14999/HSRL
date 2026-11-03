# Tuple census across folds (hsrl, 15 runs)

Counts-only bounds assume a common reader panel (not strictly true for Gleason). Linked verdicts skip pairs with < 3 shared readers. Set A (random tuples) depends only on the fold's labelled set, so it is identical across seeds within a fold.

## Set A: 100k random role-valid tuples, per fold (%)

| fold | term | ordering | pct_certified | pct_contradicted | pct_undecided | pct_supported | pct_violated | pct_tie | pct_linked_violated_given_undecided | pct_linked_violated_given_certified | pct_linked_violated_given_contradicted |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | s_ap > s_an | 96.900 | 0.000 | 3.100 | 96.000 | 1.400 | 2.600 | 27.700 | 0.600 | nan |
| 0 | 2 | s_ap > s_nc | 35.500 | 27.600 | 36.900 | 34.800 | 27.900 | 37.300 | 13.000 | 0.800 | 82.800 |
| 0 | 3 | s_ap > s_ac | 96.900 | 0.000 | 3.100 | 96.000 | 1.400 | 2.500 | 28.300 | 0.600 | nan |
| 1 | 1 | s_ap > s_an | 95.400 | 0.000 | 4.600 | 95.300 | 1.300 | 3.400 | 18.500 | 0.600 | nan |
| 1 | 2 | s_ap > s_nc | 35.400 | 27.200 | 37.400 | 36.600 | 29.900 | 33.400 | 24.000 | 1.100 | 75.400 |
| 1 | 3 | s_ap > s_ac | 95.400 | 0.000 | 4.600 | 95.200 | 1.400 | 3.400 | 20.100 | 0.600 | nan |
| 2 | 1 | s_ap > s_an | 96.700 | 0.000 | 3.300 | 96.600 | 0.800 | 2.500 | 19.000 | 0.300 | nan |
| 2 | 2 | s_ap > s_nc | 36.600 | 26.000 | 37.400 | 36.600 | 26.400 | 37.000 | 12.500 | 0.300 | 83.800 |
| 2 | 3 | s_ap > s_ac | 96.700 | 0.000 | 3.300 | 96.700 | 0.800 | 2.500 | 19.200 | 0.300 | nan |

## Set B: mined tuples (mean ± std over runs, %)

| set | term | runs | pct_certified | pct_contradicted | pct_undecided | pct_supported | pct_violated | pct_tie | pct_linked_violated_given_undecided | pct_linked_violated_given_certified | pct_linked_violated_given_contradicted | skipped_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B_mined_epoch0 | 1 | 15 | 95.795 ± 1.177 | 0.000 ± 0.000 | 4.205 ± 1.177 | 95.512 ± 0.831 | 1.359 ± 0.720 | 3.129 ± 0.696 | 19.039 ± 13.870 | 0.680 ± 0.479 | nan | 22.941 ± 2.439 |
| B_mined_epoch0 | 2 | 15 | 32.632 ± 2.377 | 29.688 ± 2.586 | 37.681 ± 2.397 | 33.277 ± 3.035 | 30.621 ± 2.588 | 36.102 ± 3.040 | 16.347 ± 5.387 | 0.729 ± 0.790 | 80.349 ± 7.303 | 26.200 ± 2.651 |
| B_mined_epoch0 | 3 | 15 | 95.830 ± 0.898 | 0.000 ± 0.000 | 4.170 ± 0.898 | 95.680 ± 1.073 | 1.380 ± 0.499 | 2.940 ± 0.845 | 20.551 ± 11.433 | 0.649 ± 0.301 | nan | 23.137 ± 2.466 |
| B_mined_epoch29 | 1 | 15 | 94.967 ± 1.243 | 0.000 ± 0.000 | 5.033 ± 1.243 | 94.794 ± 1.418 | 1.644 ± 0.693 | 3.562 ± 1.036 | 23.029 ± 12.297 | 0.689 ± 0.522 | nan | 25.535 ± 3.746 |
| B_mined_epoch29 | 2 | 15 | 34.871 ± 4.585 | 26.398 ± 2.861 | 38.732 ± 5.039 | 36.655 ± 4.807 | 28.379 ± 3.366 | 34.966 ± 3.519 | 18.968 ± 7.339 | 0.998 ± 1.433 | 78.489 ± 7.609 | 28.785 ± 4.842 |
| B_mined_epoch29 | 3 | 15 | 95.193 ± 1.591 | 0.000 ± 0.000 | 4.807 ± 1.591 | 95.222 ± 1.615 | 1.775 ± 0.829 | 3.004 ± 1.082 | 27.758 ± 11.090 | 0.662 ± 0.542 | nan | 25.471 ± 3.815 |

## Pseudo-label errors vs tuple status: CORE LEVEL (primary)

Per run: Spearman over cores (>= 5 accepted non-tie pseudo-labels) between the core's pseudo-label error rate and the mean violation (or counts-undecided) rate of its labelled patches. Partial = controlling for the core's split-vote share among accepted patches. p = core-level permutation (5000).

| rate | correlation | all runs | runs p<0.05 | fold 0 | fold 1 | fold 2 |
|---|---|---|---|---|---|---|
| viol_rate | raw | 0.166 ± 0.102 | 6/15 | 0.242 ± 0.072 | 0.181 ± 0.112 | 0.076 ± 0.027 |
| viol_rate | partial (ctrl split share) | -0.041 ± 0.095 | 0/15 | 0.040 ± 0.096 | -0.061 ± 0.093 | -0.103 ± 0.013 |
| undecided_rate | raw | 0.353 ± 0.111 | 14/15 | 0.234 ± 0.047 | 0.451 ± 0.074 | 0.373 ± 0.072 |
| undecided_rate | partial (ctrl split share) | 0.058 ± 0.062 | 0/15 | 0.035 ± 0.069 | 0.099 ± 0.042 | 0.039 ± 0.063 |

Per run:

| run | fold | seed | n_cores | n_patches | viol_rate_spearman | viol_rate_perm_p | viol_rate_partial_spearman_ctrl_split_frac | viol_rate_partial_perm_p | undecided_rate_spearman | undecided_rate_perm_p | undecided_rate_partial_spearman_ctrl_split_frac | undecided_rate_partial_perm_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0 | 0 | 113 | 3091 | 0.330 | 0.001 | 0.097 | 0.304 | 0.247 | 0.009 | 0.002 | 0.980 |
| f0s1_hsrl | 0 | 1 | 109 | 2394 | 0.139 | 0.153 | -0.088 | 0.371 | 0.154 | 0.111 | -0.047 | 0.627 |
| f0s2_hsrl | 0 | 2 | 112 | 2638 | 0.235 | 0.014 | 0.052 | 0.573 | 0.236 | 0.012 | 0.017 | 0.855 |
| f0s3_hsrl | 0 | 3 | 114 | 2980 | 0.287 | 0.003 | 0.156 | 0.094 | 0.278 | 0.002 | 0.132 | 0.156 |
| f0s4_hsrl | 0 | 4 | 109 | 2326 | 0.217 | 0.025 | -0.017 | 0.857 | 0.253 | 0.008 | 0.071 | 0.462 |
| f1s0_hsrl | 1 | 0 | 82 | 1516 | 0.263 | 0.016 | 0.068 | 0.545 | 0.468 | 0.000 | 0.117 | 0.278 |
| f1s1_hsrl | 1 | 1 | 92 | 1841 | 0.137 | 0.192 | -0.131 | 0.214 | 0.469 | 0.000 | 0.029 | 0.784 |
| f1s2_hsrl | 1 | 2 | 74 | 1274 | 0.334 | 0.005 | 0.006 | 0.966 | 0.548 | 0.000 | 0.131 | 0.256 |
| f1s3_hsrl | 1 | 3 | 76 | 1286 | 0.080 | 0.487 | -0.097 | 0.397 | 0.344 | 0.002 | 0.092 | 0.427 |
| f1s4_hsrl | 1 | 4 | 81 | 1401 | 0.093 | 0.413 | -0.149 | 0.193 | 0.428 | 0.000 | 0.126 | 0.250 |
| f2s0_hsrl | 2 | 0 | 117 | 3689 | 0.102 | 0.272 | -0.103 | 0.279 | 0.413 | 0.000 | 0.146 | 0.114 |
| f2s1_hsrl | 2 | 1 | 117 | 3642 | 0.052 | 0.589 | -0.093 | 0.314 | 0.259 | 0.005 | 0.022 | 0.819 |
| f2s2_hsrl | 2 | 2 | 116 | 3687 | 0.107 | 0.250 | -0.092 | 0.329 | 0.451 | 0.000 | 0.036 | 0.706 |
| f2s3_hsrl | 2 | 3 | 118 | 3814 | 0.050 | 0.598 | -0.124 | 0.183 | 0.360 | 0.000 | -0.018 | 0.848 |
| f2s4_hsrl | 2 | 4 | 118 | 3654 | 0.069 | 0.458 | -0.102 | 0.261 | 0.381 | 0.000 | 0.011 | 0.907 |

## Pseudo-label errors vs tuple status: PATCH LEVEL (secondary)

AUROC of the mean violation / undecided rate of the 5 nearest labelled patches (Stage I embedding) for predicting a wrong accepted pseudo-label; overall and within unanimous / split-vote patches. Patch-level p-values are optimistic (patches within a core are correlated) and are not aggregated here.

| measure | all runs | fold 0 | fold 1 | fold 2 |
|---|---|---|---|---|
| n_accepted | 2673.000 ± 951.743 | 2727.400 ± 339.709 | 1551.400 ± 224.056 | 3740.200 ± 70.151 |
| n_wrong | 213.800 ± 100.985 | 203.400 ± 43.443 | 105.400 ± 31.942 | 332.600 ± 17.883 |
| err_unanimous | 0.042 ± 0.010 | 0.043 ± 0.006 | 0.031 ± 0.004 | 0.051 ± 0.005 |
| err_split | 0.204 ± 0.030 | 0.195 ± 0.029 | 0.228 ± 0.034 | 0.189 ± 0.006 |
| nbr_viol_rate_auroc | 0.609 ± 0.029 | 0.628 ± 0.031 | 0.608 ± 0.033 | 0.592 ± 0.012 |
| nbr_viol_rate_auroc_unanimous | 0.662 ± 0.032 | 0.670 ± 0.036 | 0.650 ± 0.037 | 0.667 ± 0.024 |
| nbr_viol_rate_auroc_split_vote | 0.466 ± 0.053 | 0.481 ± 0.055 | 0.489 ± 0.056 | 0.427 ± 0.031 |
| nbr_undecided_rate_auroc | 0.594 ± 0.047 | 0.621 ± 0.038 | 0.575 ± 0.051 | 0.586 ± 0.047 |
| nbr_undecided_rate_auroc_unanimous | 0.636 ± 0.060 | 0.668 ± 0.048 | 0.601 ± 0.066 | 0.639 ± 0.054 |
| nbr_undecided_rate_auroc_split_vote | 0.479 ± 0.032 | 0.496 ± 0.024 | 0.484 ± 0.027 | 0.456 ± 0.037 |
