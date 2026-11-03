# Aggregate over results/soft, results/gleason_ext, results/gleason_margin

Runs: 18; folds [0, 1, 2]; seeds [0, 1]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl_soft | 6 | 0.795 ± 0.019 | 0.761 ± 0.024 | 0.770 ± 0.022 | 0.871 ± 0.011 | 0.158 ± 0.019 | 0.862 ± 0.013 | 0.628 ± 0.041 |
| supported_linked | 6 | 0.806 ± 0.023 | 0.784 ± 0.024 | 0.789 ± 0.023 | 0.876 ± 0.018 | 0.154 ± 0.021 | 0.867 ± 0.019 | 0.651 ± 0.029 |
| supported_gap_linked | 6 | 0.803 ± 0.030 | 0.772 ± 0.036 | 0.781 ± 0.034 | 0.873 ± 0.022 | 0.158 ± 0.026 | 0.872 ± 0.022 | 0.632 ± 0.047 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl_soft | 0 | 2 | 0.795 ± 0.010 | 0.753 ± 0.016 | 0.861 ± 0.003 | 0.623 ± 0.010 |
| hsrl_soft | 1 | 2 | 0.814 ± 0.001 | 0.784 ± 0.007 | 0.884 ± 0.001 | 0.666 ± 0.006 |
| hsrl_soft | 2 | 2 | 0.776 ± 0.016 | 0.747 ± 0.030 | 0.866 ± 0.007 | 0.595 ± 0.057 |
| supported_linked | 0 | 2 | 0.799 ± 0.003 | 0.775 ± 0.009 | 0.861 ± 0.003 | 0.660 ± 0.003 |
| supported_linked | 1 | 2 | 0.833 ± 0.002 | 0.811 ± 0.006 | 0.899 ± 0.004 | 0.675 ± 0.002 |
| supported_linked | 2 | 2 | 0.786 ± 0.015 | 0.767 ± 0.023 | 0.870 ± 0.011 | 0.617 ± 0.023 |
| supported_gap_linked | 0 | 2 | 0.790 ± 0.002 | 0.754 ± 0.008 | 0.856 ± 0.006 | 0.620 ± 0.018 |
| supported_gap_linked | 1 | 2 | 0.841 ± 0.008 | 0.817 ± 0.016 | 0.900 ± 0.015 | 0.686 ± 0.029 |
| supported_gap_linked | 2 | 2 | 0.778 ± 0.005 | 0.745 ± 0.009 | 0.864 ± 0.001 | 0.589 ± 0.008 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| supported_gap_linked − supported_linked | overall | acc | 6 | -0.002 | 0.011 | -0.014 | 0.009 | 2/6 | f0:-0.008 / f1:+0.009 / f2:-0.008 | 2 |
| supported_gap_linked − supported_linked | overall | bal_acc | 6 | -0.012 | 0.018 | -0.031 | 0.007 | 1/6 | f0:-0.021 / f1:+0.006 / f2:-0.022 | 2 |
| supported_gap_linked − supported_linked | overall | auroc | 6 | -0.003 | 0.009 | -0.013 | 0.007 | 3/6 | f0:-0.005 / f1:+0.002 / f2:-0.006 | 2 |
| supported_gap_linked − supported_linked | overall | brier | 6 | 0.003 | 0.007 | -0.004 | 0.011 | 1/6 | f0:+0.006 / f1:-0.002 / f2:+0.007 | 2 |
| supported_gap_linked − supported_linked | split_vote | acc | 6 | -0.019 | 0.029 | -0.050 | 0.012 | 1/6 | f0:-0.040 / f1:+0.011 / f2:-0.028 | 2 |
| supported_gap_linked − hsrl_soft | overall | acc | 6 | 0.008 | 0.017 | -0.010 | 0.026 | 4/6 | f0:-0.004 / f1:+0.027 / f2:+0.002 | 2 |
| supported_gap_linked − hsrl_soft | overall | bal_acc | 6 | 0.011 | 0.023 | -0.013 | 0.035 | 4/6 | f0:+0.002 / f1:+0.033 / f2:-0.002 | 2 |
| supported_gap_linked − hsrl_soft | overall | auroc | 6 | 0.003 | 0.013 | -0.011 | 0.016 | 3/6 | f0:-0.006 / f1:+0.016 / f2:-0.003 | 1 |
| supported_gap_linked − hsrl_soft | overall | brier | 6 | -0.001 | 0.009 | -0.010 | 0.009 | 3/6 | f0:+0.007 / f1:-0.009 / f2:+0.001 | 1 |
| supported_gap_linked − hsrl_soft | split_vote | acc | 6 | 0.004 | 0.032 | -0.030 | 0.038 | 3/6 | f0:-0.003 / f1:+0.020 / f2:-0.006 | 1 |

## 3. Effect of Stage III (after − before, paired within run)

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | acc | 6 | 0.016 | 0.016 | 0.000 | 0.033 | 5/6 | f0:+0.014 / f1:+0.033 / f2:+0.002 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | bal_acc | 6 | 0.014 | 0.023 | -0.010 | 0.039 | 5/6 | f0:+0.010 / f1:+0.036 / f2:-0.002 | 2 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | auroc | 6 | 0.014 | 0.013 | 0.000 | 0.027 | 6/6 | f0:+0.008 / f1:+0.029 / f2:+0.005 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | unanimous | acc | 6 | 0.019 | 0.013 | 0.005 | 0.033 | 6/6 | f0:+0.019 / f1:+0.033 / f2:+0.005 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | split_vote | acc | 6 | 0.010 | 0.033 | -0.025 | 0.045 | 4/6 | f0:+0.002 / f1:+0.033 / f2:-0.004 | 2 |

### Every run: before (pre) / after (post) Stage III

| run | pre_acc | pre_bal_acc | pre_split_vote_acc | pre_unanimous_acc | post_acc | post_bal_acc | post_split_vote_acc | post_unanimous_acc |
|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl_soft | 0.790 | 0.761 | 0.648 | 0.854 | 0.802 | 0.764 | 0.631 | 0.878 |
| f0s1_hsrl_soft | 0.771 | 0.725 | 0.595 | 0.850 | 0.787 | 0.741 | 0.616 | 0.864 |
| f1s0_hsrl_soft | 0.780 | 0.744 | 0.639 | 0.832 | 0.815 | 0.779 | 0.670 | 0.868 |
| f1s1_hsrl_soft | 0.781 | 0.752 | 0.627 | 0.838 | 0.813 | 0.788 | 0.662 | 0.869 |
| f2s0_hsrl_soft | 0.774 | 0.748 | 0.599 | 0.842 | 0.787 | 0.769 | 0.635 | 0.846 |
| f2s1_hsrl_soft | 0.774 | 0.751 | 0.599 | 0.841 | 0.765 | 0.726 | 0.555 | 0.846 |

## 4. Stage III pseudo-labels (vs hidden majority labels)

| config | runs | coverage | precision | prec_unanimous | prec_split | min_coverage |
|---|---|---|---|---|---|---|
| hsrl_soft | 6 | 0.464 ± 0.075 | 0.944 ± 0.015 | 0.976 ± 0.008 | 0.792 ± 0.058 | 0.347 |
| supported_linked | 6 | 0.521 ± 0.040 | 0.951 ± 0.012 | 0.980 ± 0.005 | 0.827 ± 0.044 | 0.466 |
| supported_gap_linked | 6 | 0.534 ± 0.046 | 0.949 ± 0.008 | 0.979 ± 0.003 | 0.823 ± 0.026 | 0.481 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl_soft | 6 | 30 | 6/6 | 2/6 | 16 17 | 0.039 ± 0.025 | 0.620 ± 0.824 | 0.826 ± 0.030 | 0.71/0.80/0.68 |
| supported_linked | 6 | 30 | 4/6 | 4/6 | 19 20 25 23 | 0.065 ± 0.029 | 1.581 ± 0.185 | 0.833 ± 0.035 | 0.19/0.10/0.04 |
| supported_gap_linked | 6 | 30 | 4/6 | 4/6 | 20 20 26 23 | 0.063 ± 0.030 | 1.271 ± 0.118 | 0.833 ± 0.017 | 0.19/0.06/0.04 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl_soft | 0.761 | 0.028 | 21 | 6.000 | nan | 0.300 | 0.873 |
| f0s1_hsrl_soft | 0.699 | 0.023 | 24 | 6.000 | nan | 0.029 | 0.819 |
| f1s0_hsrl_soft | 0.732 | 0.018 | 29 | 6.000 | nan | 0.018 | 0.802 |
| f1s1_hsrl_soft | 0.665 | 0.023 | 29 | 8.000 | nan | 0.023 | 0.808 |
| f2s0_hsrl_soft | 0.771 | 0.076 | 10 | 10.000 | 16.000 | 1.711 | 0.803 |
| f2s1_hsrl_soft | 0.695 | 0.065 | 11 | 9.000 | 17.000 | 1.637 | 0.852 |
| f0s0_supported_linked | 0.761 | 0.051 | 12 | 6.000 | 19.000 | 1.690 | 0.884 |
| f0s1_supported_linked | 0.699 | 0.046 | 13 | 7.000 | 20.000 | 1.520 | 0.834 |
| f1s0_supported_linked | 0.732 | 0.041 | 18 | 7.000 | 25.000 | 1.310 | 0.799 |
| f1s1_supported_linked | 0.665 | 0.047 | 16 | 9.000 | 23.000 | 1.454 | 0.787 |
| f2s0_supported_linked | 0.771 | 0.104 | 6 | nan | nan | 1.802 | 0.841 |
| f2s1_supported_linked | 0.695 | 0.100 | 7 | nan | nan | 1.712 | 0.852 |
| f0s0_supported_gap_linked | 0.761 | 0.047 | 13 | 6.000 | 20.000 | 1.236 | 0.827 |
| f0s1_supported_gap_linked | 0.699 | 0.045 | 13 | 7.000 | 20.000 | 1.151 | 0.851 |
| f1s0_supported_gap_linked | 0.732 | 0.038 | 18 | 6.000 | 26.000 | 1.218 | 0.807 |
| f1s1_supported_gap_linked | 0.665 | 0.048 | 16 | 10.000 | 23.000 | 1.193 | 0.848 |
| f2s0_supported_gap_linked | 0.771 | 0.100 | 6 | nan | nan | 1.463 | 0.826 |
| f2s1_supported_gap_linked | 0.695 | 0.102 | 6 | nan | nan | 1.365 | 0.842 |
