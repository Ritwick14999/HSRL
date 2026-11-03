# Tuple census across folds (hsrl_s1e60, 15 runs)

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
| B_mined_epoch59 | 1 | 15 | 94.360 ± 1.277 | 0.000 ± 0.000 | 5.640 ± 1.277 | 95.083 ± 1.305 | 1.492 ± 0.505 | 3.424 ± 1.379 | 19.596 ± 7.137 | 0.494 ± 0.296 | nan | 24.075 ± 5.746 |
| B_mined_epoch59 | 2 | 15 | 34.435 ± 4.267 | 27.123 ± 3.748 | 38.442 ± 3.985 | 37.177 ± 6.444 | 29.019 ± 3.096 | 33.803 ± 4.449 | 19.165 ± 5.711 | 1.033 ± 0.987 | 79.457 ± 6.789 | 28.269 ± 7.059 |
| B_mined_epoch59 | 3 | 15 | 95.427 ± 1.252 | 0.000 ± 0.000 | 4.573 ± 1.252 | 95.269 ± 1.502 | 1.233 ± 0.487 | 3.497 ± 1.322 | 22.801 ± 10.236 | 0.378 ± 0.380 | nan | 22.437 ± 3.575 |

## Pseudo-label errors vs tuple status: CORE LEVEL (primary)

Per run: Spearman over cores (>= 5 accepted non-tie pseudo-labels) between the core's pseudo-label error rate and the mean violation (or counts-undecided) rate of its labelled patches. Partial = controlling for the core's split-vote share among accepted patches. p = core-level permutation (5000).

| rate | correlation | all runs | runs p<0.05 | fold 0 | fold 1 | fold 2 |
|---|---|---|---|---|---|---|
| viol_rate | raw | 0.221 ± 0.109 | 8/15 | 0.338 ± 0.040 | 0.220 ± 0.054 | 0.104 ± 0.055 |
| viol_rate | partial (ctrl split share) | 0.027 ± 0.106 | 0/15 | 0.119 ± 0.043 | 0.053 ± 0.066 | -0.091 ± 0.069 |
| undecided_rate | raw | 0.421 ± 0.093 | 15/15 | 0.355 ± 0.027 | 0.534 ± 0.050 | 0.373 ± 0.049 |
| undecided_rate | partial (ctrl split share) | 0.143 ± 0.107 | 5/15 | 0.151 ± 0.042 | 0.250 ± 0.081 | 0.029 ± 0.027 |

Per run:

| run | fold | seed | n_cores | n_patches | viol_rate_spearman | viol_rate_perm_p | viol_rate_partial_spearman_ctrl_split_frac | viol_rate_partial_perm_p | undecided_rate_spearman | undecided_rate_perm_p | undecided_rate_partial_spearman_ctrl_split_frac | undecided_rate_partial_perm_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl_s1e60 | 0 | 0 | 114 | 3553 | 0.376 | 0.000 | 0.124 | 0.184 | 0.344 | 0.000 | 0.105 | 0.267 |
| f0s1_hsrl_s1e60 | 0 | 1 | 113 | 3466 | 0.336 | 0.000 | 0.123 | 0.191 | 0.354 | 0.000 | 0.173 | 0.062 |
| f0s2_hsrl_s1e60 | 0 | 2 | 113 | 3488 | 0.304 | 0.000 | 0.111 | 0.242 | 0.350 | 0.000 | 0.173 | 0.064 |
| f0s3_hsrl_s1e60 | 0 | 3 | 114 | 3573 | 0.382 | 0.000 | 0.178 | 0.064 | 0.400 | 0.000 | 0.197 | 0.038 |
| f0s4_hsrl_s1e60 | 0 | 4 | 114 | 3437 | 0.294 | 0.002 | 0.059 | 0.536 | 0.326 | 0.000 | 0.107 | 0.256 |
| f1s0_hsrl_s1e60 | 1 | 0 | 110 | 3257 | 0.235 | 0.019 | 0.044 | 0.652 | 0.593 | 0.000 | 0.329 | 0.000 |
| f1s1_hsrl_s1e60 | 1 | 1 | 110 | 3352 | 0.157 | 0.091 | -0.027 | 0.775 | 0.508 | 0.000 | 0.230 | 0.014 |
| f1s2_hsrl_s1e60 | 1 | 2 | 109 | 2895 | 0.284 | 0.003 | 0.151 | 0.114 | 0.540 | 0.000 | 0.334 | 0.000 |
| f1s3_hsrl_s1e60 | 1 | 3 | 109 | 3043 | 0.173 | 0.070 | 0.022 | 0.823 | 0.466 | 0.000 | 0.142 | 0.140 |
| f1s4_hsrl_s1e60 | 1 | 4 | 110 | 3242 | 0.252 | 0.009 | 0.074 | 0.448 | 0.565 | 0.000 | 0.216 | 0.021 |
| f2s0_hsrl_s1e60 | 2 | 0 | 118 | 3710 | 0.121 | 0.179 | -0.108 | 0.237 | 0.391 | 0.000 | 0.033 | 0.729 |
| f2s1_hsrl_s1e60 | 2 | 1 | 116 | 3783 | 0.122 | 0.196 | -0.051 | 0.591 | 0.291 | 0.001 | 0.030 | 0.742 |
| f2s2_hsrl_s1e60 | 2 | 2 | 118 | 3810 | 0.016 | 0.857 | -0.178 | 0.053 | 0.409 | 0.000 | 0.039 | 0.673 |
| f2s3_hsrl_s1e60 | 2 | 3 | 117 | 3855 | 0.098 | 0.290 | -0.119 | 0.199 | 0.370 | 0.000 | -0.016 | 0.867 |
| f2s4_hsrl_s1e60 | 2 | 4 | 118 | 3812 | 0.165 | 0.076 | 0.001 | 0.989 | 0.405 | 0.000 | 0.057 | 0.537 |

## Pseudo-label errors vs tuple status: PATCH LEVEL (secondary)

AUROC of the mean violation / undecided rate of the 5 nearest labelled patches (Stage I embedding) for predicting a wrong accepted pseudo-label; overall and within unanimous / split-vote patches. Patch-level p-values are optimistic (patches within a core are correlated) and are not aggregated here.

| measure | all runs | fold 0 | fold 1 | fold 2 |
|---|---|---|---|---|
| n_accepted | 3528.400 ± 294.921 | 3552.000 ± 58.009 | 3192.600 ± 185.099 | 3840.600 ± 57.570 |
| n_wrong | 343.333 ± 31.618 | 345.200 ± 9.602 | 361.000 ± 49.071 | 323.800 ± 11.278 |
| err_unanimous | 0.058 ± 0.012 | 0.061 ± 0.003 | 0.069 ± 0.010 | 0.044 ± 0.003 |
| err_split | 0.204 ± 0.016 | 0.202 ± 0.008 | 0.220 ± 0.014 | 0.191 ± 0.009 |
| nbr_viol_rate_auroc | 0.563 ± 0.044 | 0.524 ± 0.038 | 0.599 ± 0.019 | 0.566 ± 0.038 |
| nbr_viol_rate_auroc_unanimous | 0.610 ± 0.066 | 0.538 ± 0.048 | 0.637 ± 0.028 | 0.655 ± 0.045 |
| nbr_viol_rate_auroc_split_vote | 0.450 ± 0.055 | 0.460 ± 0.028 | 0.500 ± 0.038 | 0.389 ± 0.023 |
| nbr_undecided_rate_auroc | 0.606 ± 0.034 | 0.609 ± 0.024 | 0.627 ± 0.025 | 0.581 ± 0.037 |
| nbr_undecided_rate_auroc_unanimous | 0.655 ± 0.027 | 0.646 ± 0.026 | 0.665 ± 0.031 | 0.653 ± 0.025 |
| nbr_undecided_rate_auroc_split_vote | 0.481 ± 0.051 | 0.502 ± 0.028 | 0.518 ± 0.020 | 0.424 ± 0.039 |
