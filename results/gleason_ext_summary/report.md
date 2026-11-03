# Aggregate over results/soft, results/gleason_ext

Runs: 30; folds [0, 1, 2]; seeds [0, 1]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl_soft | 6 | 0.795 ± 0.019 | 0.761 ± 0.024 | 0.770 ± 0.022 | 0.871 ± 0.011 | 0.158 ± 0.019 | 0.862 ± 0.013 | 0.628 ± 0.041 |
| supervised_soft | 6 | 0.799 ± 0.024 | 0.782 ± 0.026 | 0.784 ± 0.024 | 0.873 ± 0.023 | 0.142 ± 0.016 | 0.857 ± 0.023 | 0.655 ± 0.025 |
| supported_counts | 6 | 0.804 ± 0.019 | 0.779 ± 0.027 | 0.784 ± 0.023 | 0.873 ± 0.016 | 0.157 ± 0.018 | 0.867 ± 0.010 | 0.647 ± 0.041 |
| supported_linked | 6 | 0.806 ± 0.023 | 0.784 ± 0.024 | 0.789 ± 0.023 | 0.876 ± 0.018 | 0.154 ± 0.021 | 0.867 ± 0.019 | 0.651 ± 0.029 |
| supported_permuted | 6 | 0.805 ± 0.024 | 0.778 ± 0.030 | 0.785 ± 0.027 | 0.876 ± 0.026 | 0.155 ± 0.023 | 0.867 ± 0.016 | 0.649 ± 0.038 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl_soft | 0 | 2 | 0.795 ± 0.010 | 0.753 ± 0.016 | 0.861 ± 0.003 | 0.623 ± 0.010 |
| supervised_soft | 0 | 2 | 0.794 ± 0.002 | 0.767 ± 0.007 | 0.867 ± 0.002 | 0.653 ± 0.003 |
| hsrl_soft | 1 | 2 | 0.814 ± 0.001 | 0.784 ± 0.007 | 0.884 ± 0.001 | 0.666 ± 0.006 |
| supervised_soft | 1 | 2 | 0.828 ± 0.003 | 0.814 ± 0.012 | 0.900 ± 0.001 | 0.682 ± 0.013 |
| hsrl_soft | 2 | 2 | 0.776 ± 0.016 | 0.747 ± 0.030 | 0.866 ± 0.007 | 0.595 ± 0.057 |
| supervised_soft | 2 | 2 | 0.776 ± 0.005 | 0.764 ± 0.003 | 0.851 ± 0.003 | 0.630 ± 0.017 |
| supported_counts | 0 | 2 | 0.796 ± 0.000 | 0.769 ± 0.000 | 0.859 ± 0.008 | 0.634 ± 0.013 |
| supported_linked | 0 | 2 | 0.799 ± 0.003 | 0.775 ± 0.009 | 0.861 ± 0.003 | 0.660 ± 0.003 |
| supported_permuted | 0 | 2 | 0.790 ± 0.014 | 0.757 ± 0.016 | 0.849 ± 0.010 | 0.629 ± 0.013 |
| supported_counts | 1 | 2 | 0.828 ± 0.009 | 0.813 ± 0.000 | 0.892 ± 0.005 | 0.697 ± 0.015 |
| supported_linked | 1 | 2 | 0.833 ± 0.002 | 0.811 ± 0.006 | 0.899 ± 0.004 | 0.675 ± 0.002 |
| supported_permuted | 1 | 2 | 0.834 ± 0.003 | 0.815 ± 0.011 | 0.905 ± 0.005 | 0.697 ± 0.012 |
| supported_counts | 2 | 2 | 0.787 ± 0.003 | 0.755 ± 0.001 | 0.869 ± 0.005 | 0.611 ± 0.002 |
| supported_linked | 2 | 2 | 0.786 ± 0.015 | 0.767 ± 0.023 | 0.870 ± 0.011 | 0.617 ± 0.023 |
| supported_permuted | 2 | 2 | 0.790 ± 0.002 | 0.762 ± 0.007 | 0.874 ± 0.001 | 0.623 ± 0.003 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| supported_linked − supported_permuted | overall | acc | 6 | 0.001 | 0.010 | -0.009 | 0.011 | 4/6 | f0:+0.008 / f1:-0.002 / f2:-0.003 | 1 |
| supported_linked − supported_permuted | overall | bal_acc | 6 | 0.006 | 0.017 | -0.011 | 0.024 | 3/6 | f0:+0.018 / f1:-0.004 / f2:+0.005 | 2 |
| supported_linked − supported_permuted | overall | auroc | 6 | 0.000 | 0.012 | -0.012 | 0.013 | 3/6 | f0:+0.012 / f1:-0.007 / f2:-0.004 | 1 |
| supported_linked − supported_permuted | overall | brier | 6 | -0.001 | 0.007 | -0.008 | 0.006 | 4/6 | f0:-0.006 / f1:+0.002 / f2:+0.002 | 1 |
| supported_linked − supported_permuted | split_vote | acc | 6 | 0.001 | 0.028 | -0.028 | 0.030 | 3/6 | f0:+0.032 / f1:-0.022 / f2:-0.006 | 1 |
| supported_linked − supported_counts | overall | acc | 6 | 0.002 | 0.009 | -0.008 | 0.012 | 4/6 | f0:+0.002 / f1:+0.005 / f2:-0.001 | 2 |
| supported_linked − supported_counts | overall | bal_acc | 6 | 0.005 | 0.014 | -0.009 | 0.020 | 4/6 | f0:+0.006 / f1:-0.002 / f2:+0.013 | 2 |
| supported_linked − supported_counts | overall | auroc | 6 | 0.003 | 0.009 | -0.007 | 0.013 | 4/6 | f0:+0.001 / f1:+0.007 / f2:+0.001 | 3 |
| supported_linked − supported_counts | overall | brier | 6 | -0.002 | 0.007 | -0.010 | 0.006 | 3/6 | f0:+0.002 / f1:-0.007 / f2:-0.001 | 2 |
| supported_linked − supported_counts | split_vote | acc | 6 | 0.003 | 0.026 | -0.024 | 0.031 | 3/6 | f0:+0.026 / f1:-0.022 / f2:+0.006 | 2 |
| supported_permuted − supported_counts | overall | acc | 6 | 0.001 | 0.010 | -0.010 | 0.012 | 3/6 | f0:-0.006 / f1:+0.006 / f2:+0.002 | 2 |
| supported_permuted − supported_counts | overall | bal_acc | 6 | -0.001 | 0.013 | -0.015 | 0.013 | 3/6 | f0:-0.012 / f1:+0.002 / f2:+0.007 | 1 |
| supported_permuted − supported_counts | overall | auroc | 6 | 0.002 | 0.015 | -0.013 | 0.018 | 5/6 | f0:-0.011 / f1:+0.014 / f2:+0.004 | 2 |
| supported_permuted − supported_counts | overall | brier | 6 | -0.001 | 0.010 | -0.012 | 0.009 | 3/6 | f0:+0.008 / f1:-0.008 / f2:-0.003 | 2 |
| supported_permuted − supported_counts | split_vote | acc | 6 | 0.002 | 0.008 | -0.007 | 0.011 | 3/6 | f0:-0.006 / f1:+0.000 / f2:+0.012 | 1 |
| supported_linked − hsrl_soft | overall | acc | 6 | 0.011 | 0.007 | 0.003 | 0.019 | 5/6 | f0:+0.004 / f1:+0.019 / f2:+0.010 | 3 |
| supported_linked − hsrl_soft | overall | bal_acc | 6 | 0.023 | 0.013 | 0.009 | 0.037 | 6/6 | f0:+0.022 / f1:+0.027 / f2:+0.020 | 3 |
| supported_linked − hsrl_soft | overall | auroc | 6 | 0.006 | 0.008 | -0.003 | 0.014 | 5/6 | f0:-0.001 / f1:+0.014 / f2:+0.003 | 2 |
| supported_linked − hsrl_soft | overall | brier | 6 | -0.004 | 0.004 | -0.008 | 0.000 | 5/6 | f0:+0.001 / f1:-0.007 / f2:-0.005 | 2 |
| supported_linked − hsrl_soft | split_vote | acc | 6 | 0.023 | 0.020 | 0.001 | 0.044 | 5/6 | f0:+0.037 / f1:+0.009 / f2:+0.022 | 3 |
| supported_permuted − hsrl_soft | overall | acc | 6 | 0.010 | 0.013 | -0.004 | 0.024 | 4/6 | f0:-0.004 / f1:+0.020 / f2:+0.013 | 2 |
| supported_permuted − hsrl_soft | overall | bal_acc | 6 | 0.017 | 0.018 | -0.002 | 0.036 | 5/6 | f0:+0.004 / f1:+0.032 / f2:+0.015 | 3 |
| supported_permuted − hsrl_soft | overall | auroc | 6 | 0.005 | 0.016 | -0.012 | 0.022 | 4/6 | f0:-0.013 / f1:+0.021 / f2:+0.007 | 2 |
| supported_permuted − hsrl_soft | overall | brier | 6 | -0.003 | 0.009 | -0.013 | 0.007 | 4/6 | f0:+0.007 / f1:-0.009 / f2:-0.007 | 2 |
| supported_permuted − hsrl_soft | split_vote | acc | 6 | 0.021 | 0.027 | -0.007 | 0.050 | 5/6 | f0:+0.005 / f1:+0.031 / f2:+0.028 | 3 |
| supported_counts − hsrl_soft | overall | acc | 6 | 0.009 | 0.012 | -0.003 | 0.021 | 4/6 | f0:+0.002 / f1:+0.014 / f2:+0.011 | 3 |
| supported_counts − hsrl_soft | overall | bal_acc | 6 | 0.018 | 0.019 | -0.002 | 0.038 | 5/6 | f0:+0.016 / f1:+0.030 / f2:+0.007 | 3 |
| supported_counts − hsrl_soft | overall | auroc | 6 | 0.003 | 0.009 | -0.007 | 0.012 | 4/6 | f0:-0.002 / f1:+0.008 / f2:+0.003 | 2 |
| supported_counts − hsrl_soft | overall | brier | 6 | -0.002 | 0.007 | -0.010 | 0.006 | 3/6 | f0:-0.001 / f1:-0.000 / f2:-0.004 | 3 |
| supported_counts − hsrl_soft | split_vote | acc | 6 | 0.019 | 0.028 | -0.010 | 0.049 | 5/6 | f0:+0.011 / f1:+0.031 / f2:+0.017 | 3 |

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
| supported_counts | 6 | 0.520 ± 0.050 | 0.954 ± 0.011 | 0.980 ± 0.004 | 0.841 ± 0.037 | 0.456 |
| supported_linked | 6 | 0.521 ± 0.040 | 0.951 ± 0.012 | 0.980 ± 0.005 | 0.827 ± 0.044 | 0.466 |
| supported_permuted | 6 | 0.521 ± 0.050 | 0.951 ± 0.009 | 0.979 ± 0.005 | 0.829 ± 0.027 | 0.460 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl_soft | 6 | 30 | 6/6 | 2/6 | 16 17 | 0.039 ± 0.025 | 0.620 ± 0.824 | 0.826 ± 0.030 | 0.71/0.80/0.68 |
| supported_counts | 6 | 30 | 4/6 | 4/6 | 19 20 24 22 | 0.066 ± 0.028 | 1.552 ± 0.244 | 0.837 ± 0.023 | 0.14/0.13/0.04 |
| supported_linked | 6 | 30 | 4/6 | 4/6 | 19 20 25 23 | 0.065 ± 0.029 | 1.581 ± 0.185 | 0.833 ± 0.035 | 0.19/0.10/0.04 |
| supported_permuted | 6 | 30 | 4/6 | 4/6 | 19 19 25 22 | 0.065 ± 0.027 | 1.522 ± 0.219 | 0.832 ± 0.015 | 0.19/0.10/0.05 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl_soft | 0.761 | 0.028 | 21 | 6.000 | nan | 0.300 | 0.873 |
| f0s1_hsrl_soft | 0.699 | 0.023 | 24 | 6.000 | nan | 0.029 | 0.819 |
| f1s0_hsrl_soft | 0.732 | 0.018 | 29 | 6.000 | nan | 0.018 | 0.802 |
| f1s1_hsrl_soft | 0.665 | 0.023 | 29 | 8.000 | nan | 0.023 | 0.808 |
| f2s0_hsrl_soft | 0.771 | 0.076 | 10 | 10.000 | 16.000 | 1.711 | 0.803 |
| f2s1_hsrl_soft | 0.695 | 0.065 | 11 | 9.000 | 17.000 | 1.637 | 0.852 |
| f0s0_supported_counts | 0.761 | 0.050 | 12 | 6.000 | 19.000 | 1.627 | 0.876 |
| f0s0_supported_linked | 0.761 | 0.051 | 12 | 6.000 | 19.000 | 1.690 | 0.884 |
| f0s0_supported_permuted | 0.761 | 0.050 | 12 | 6.000 | 19.000 | 1.402 | 0.845 |
| f0s1_supported_counts | 0.699 | 0.047 | 12 | 7.000 | 20.000 | 1.632 | 0.811 |
| f0s1_supported_linked | 0.699 | 0.046 | 13 | 7.000 | 20.000 | 1.520 | 0.834 |
| f0s1_supported_permuted | 0.699 | 0.047 | 13 | 7.000 | 19.000 | 1.618 | 0.849 |
| f1s0_supported_counts | 0.732 | 0.043 | 15 | 7.000 | 24.000 | 1.100 | 0.846 |
| f1s0_supported_linked | 0.732 | 0.041 | 18 | 7.000 | 25.000 | 1.310 | 0.799 |
| f1s0_supported_permuted | 0.732 | 0.042 | 18 | 7.000 | 25.000 | 1.181 | 0.831 |
| f1s1_supported_counts | 0.665 | 0.052 | 16 | 10.000 | 22.000 | 1.468 | 0.818 |
| f1s1_supported_linked | 0.665 | 0.047 | 16 | 9.000 | 23.000 | 1.454 | 0.787 |
| f1s1_supported_permuted | 0.665 | 0.052 | 14 | 10.000 | 22.000 | 1.463 | 0.829 |
| f2s0_supported_counts | 0.771 | 0.106 | 6 | nan | nan | 1.755 | 0.833 |
| f2s0_supported_linked | 0.771 | 0.104 | 6 | nan | nan | 1.802 | 0.841 |
| f2s0_supported_permuted | 0.771 | 0.102 | 6 | nan | nan | 1.791 | 0.807 |
| f2s1_supported_counts | 0.695 | 0.098 | 6 | nan | nan | 1.734 | 0.841 |
| f2s1_supported_linked | 0.695 | 0.100 | 7 | nan | nan | 1.712 | 0.852 |
| f2s1_supported_permuted | 0.695 | 0.098 | 6 | nan | nan | 1.675 | 0.828 |
