# Aggregate over results/mhist_randsplit

Runs: 20; folds [0, 1, 2, 3, 4]; seeds [0, 1, 2, 3, 4]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl | 5 | 0.822 ± 0.016 | 0.788 ± 0.018 | 0.791 ± 0.017 | 0.881 ± 0.014 | 0.139 ± 0.012 | 0.923 ± 0.013 | 0.770 ± 0.020 |
| hsrl_no_stage1 | 5 | 0.752 ± 0.014 | 0.713 ± 0.017 | 0.712 ± 0.015 | 0.812 ± 0.008 | 0.165 ± 0.002 | 0.839 ± 0.020 | 0.707 ± 0.019 |
| supervised | 5 | 0.816 ± 0.025 | 0.792 ± 0.024 | 0.789 ± 0.027 | 0.880 ± 0.016 | 0.147 ± 0.020 | 0.923 ± 0.015 | 0.762 ± 0.035 |
| supervised_full | 5 | 0.883 ± 0.008 | 0.859 ± 0.010 | 0.863 ± 0.009 | 0.932 ± 0.010 | 0.097 ± 0.005 | 0.974 ± 0.008 | 0.836 ± 0.018 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl | 0 | 1 | 0.826 | 0.779 | 0.880 | 0.773 |
| hsrl_no_stage1 | 0 | 1 | 0.766 | 0.731 | 0.821 | 0.714 |
| supervised | 0 | 1 | 0.827 | 0.788 | 0.884 | 0.770 |
| supervised_full | 0 | 1 | 0.881 | 0.853 | 0.932 | 0.838 |
| hsrl | 1 | 1 | 0.841 | 0.801 | 0.897 | 0.797 |
| hsrl_no_stage1 | 1 | 1 | 0.741 | 0.694 | 0.816 | 0.697 |
| supervised | 1 | 1 | 0.845 | 0.823 | 0.889 | 0.803 |
| supervised_full | 1 | 1 | 0.880 | 0.859 | 0.925 | 0.832 |
| hsrl | 2 | 1 | 0.830 | 0.813 | 0.889 | 0.780 |
| hsrl_no_stage1 | 2 | 1 | 0.765 | 0.723 | 0.813 | 0.729 |
| supervised | 2 | 1 | 0.825 | 0.807 | 0.893 | 0.781 |
| supervised_full | 2 | 1 | 0.887 | 0.863 | 0.942 | 0.849 |
| hsrl | 3 | 1 | 0.803 | 0.779 | 0.881 | 0.746 |
| hsrl_no_stage1 | 3 | 1 | 0.733 | 0.719 | 0.812 | 0.680 |
| supervised | 3 | 1 | 0.803 | 0.781 | 0.879 | 0.740 |
| supervised_full | 3 | 1 | 0.872 | 0.848 | 0.919 | 0.808 |
| hsrl | 4 | 1 | 0.807 | 0.771 | 0.858 | 0.754 |
| hsrl_no_stage1 | 4 | 1 | 0.754 | 0.696 | 0.800 | 0.716 |
| supervised | 4 | 1 | 0.779 | 0.760 | 0.854 | 0.715 |
| supervised_full | 4 | 1 | 0.892 | 0.873 | 0.941 | 0.853 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl − supervised | overall | acc | 5 | 0.006 | 0.013 | -0.010 | 0.021 | 2/5 | f0:-0.001 / f1:-0.004 / f2:+0.005 / f3:+0.000 / f4:+0.028 | 2 |
| hsrl − supervised | overall | bal_acc | 5 | -0.003 | 0.013 | -0.019 | 0.012 | 2/5 | f0:-0.010 / f1:-0.021 / f2:+0.005 / f3:-0.002 / f4:+0.010 | 3 |
| hsrl − supervised | overall | auroc | 5 | 0.001 | 0.005 | -0.005 | 0.008 | 3/5 | f0:-0.004 / f1:+0.008 / f2:-0.004 / f3:+0.002 / f4:+0.005 | 3 |
| hsrl − supervised | overall | brier | 5 | -0.008 | 0.010 | -0.021 | 0.004 | 5/5 | f0:-0.007 / f1:-0.001 / f2:-0.006 / f3:-0.003 / f4:-0.026 | 5 |
| hsrl − supervised | split_vote | acc | 5 | 0.008 | 0.018 | -0.014 | 0.031 | 3/5 | f0:+0.003 / f1:-0.006 / f2:-0.002 / f3:+0.006 / f4:+0.040 | 3 |
| hsrl − hsrl_no_stage1 | overall | acc | 5 | 0.070 | 0.018 | 0.047 | 0.093 | 5/5 | f0:+0.060 / f1:+0.100 / f2:+0.066 / f3:+0.071 / f4:+0.052 | 5 |
| hsrl − hsrl_no_stage1 | overall | bal_acc | 5 | 0.076 | 0.024 | 0.047 | 0.105 | 5/5 | f0:+0.047 / f1:+0.108 / f2:+0.089 / f3:+0.060 / f4:+0.075 | 5 |
| hsrl − hsrl_no_stage1 | overall | auroc | 5 | 0.069 | 0.010 | 0.056 | 0.081 | 5/5 | f0:+0.059 / f1:+0.081 / f2:+0.076 / f3:+0.069 / f4:+0.059 | 5 |
| hsrl − hsrl_no_stage1 | overall | brier | 5 | -0.026 | 0.010 | -0.039 | -0.013 | 5/5 | f0:-0.029 / f1:-0.039 / f2:-0.030 / f3:-0.019 / f4:-0.013 | 5 |
| hsrl − hsrl_no_stage1 | split_vote | acc | 5 | 0.063 | 0.023 | 0.034 | 0.092 | 5/5 | f0:+0.059 / f1:+0.100 / f2:+0.051 / f3:+0.066 / f4:+0.038 | 5 |
| hsrl_no_stage1 − supervised | overall | acc | 5 | -0.064 | 0.029 | -0.100 | -0.029 | 0/5 | f0:-0.061 / f1:-0.104 / f2:-0.060 / f3:-0.071 / f4:-0.025 | 5 |
| hsrl_no_stage1 − supervised | overall | bal_acc | 5 | -0.079 | 0.030 | -0.116 | -0.043 | 0/5 | f0:-0.057 / f1:-0.129 / f2:-0.084 / f3:-0.062 / f4:-0.065 | 5 |
| hsrl_no_stage1 − supervised | overall | auroc | 5 | -0.068 | 0.010 | -0.080 | -0.055 | 0/5 | f0:-0.064 / f1:-0.074 / f2:-0.080 / f3:-0.067 / f4:-0.054 | 5 |
| hsrl_no_stage1 − supervised | overall | brier | 5 | 0.018 | 0.019 | -0.006 | 0.041 | 1/5 | f0:+0.022 / f1:+0.039 / f2:+0.024 / f3:+0.016 / f4:-0.013 | 4 |
| hsrl_no_stage1 − supervised | split_vote | acc | 5 | -0.054 | 0.038 | -0.102 | -0.007 | 1/5 | f0:-0.056 / f1:-0.106 / f2:-0.052 / f3:-0.059 / f4:+0.001 | 4 |
| supervised_full − supervised | overall | acc | 5 | 0.067 | 0.029 | 0.031 | 0.103 | 5/5 | f0:+0.054 / f1:+0.035 / f2:+0.062 / f3:+0.069 / f4:+0.114 | 5 |
| supervised_full − supervised | overall | bal_acc | 5 | 0.067 | 0.028 | 0.032 | 0.102 | 5/5 | f0:+0.065 / f1:+0.036 / f2:+0.056 / f3:+0.067 / f4:+0.113 | 5 |
| supervised_full − supervised | overall | auroc | 5 | 0.052 | 0.020 | 0.026 | 0.077 | 5/5 | f0:+0.048 / f1:+0.035 / f2:+0.049 / f3:+0.040 / f4:+0.087 | 5 |
| supervised_full − supervised | overall | brier | 5 | -0.050 | 0.022 | -0.077 | -0.022 | 5/5 | f0:-0.040 / f1:-0.025 / f2:-0.047 / f3:-0.052 / f4:-0.085 | 5 |
| supervised_full − supervised | split_vote | acc | 5 | 0.075 | 0.040 | 0.025 | 0.124 | 5/5 | f0:+0.068 / f1:+0.029 / f2:+0.068 / f3:+0.069 / f4:+0.139 | 5 |
| supervised_full − hsrl | overall | acc | 5 | 0.061 | 0.017 | 0.040 | 0.083 | 5/5 | f0:+0.055 / f1:+0.039 / f2:+0.057 / f3:+0.069 / f4:+0.086 | 5 |
| supervised_full − hsrl | overall | bal_acc | 5 | 0.071 | 0.020 | 0.046 | 0.096 | 5/5 | f0:+0.075 / f1:+0.057 / f2:+0.051 / f3:+0.069 / f4:+0.102 | 5 |
| supervised_full − hsrl | overall | auroc | 5 | 0.051 | 0.020 | 0.025 | 0.076 | 5/5 | f0:+0.052 / f1:+0.028 / f2:+0.053 / f3:+0.038 / f4:+0.082 | 5 |
| supervised_full − hsrl | overall | brier | 5 | -0.041 | 0.013 | -0.058 | -0.024 | 5/5 | f0:-0.033 / f1:-0.024 / f2:-0.042 / f3:-0.049 / f4:-0.058 | 5 |
| supervised_full − hsrl | split_vote | acc | 5 | 0.066 | 0.023 | 0.038 | 0.094 | 5/5 | f0:+0.065 / f1:+0.035 / f2:+0.069 / f3:+0.062 / f4:+0.099 | 5 |

## 3. Effect of Stage III (after − before, paired within run)

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl[final] − hsrl[before_stage3] | overall | acc | 5 | 0.012 | 0.010 | 0.000 | 0.024 | 5/5 | f0:+0.007 / f1:+0.004 / f2:+0.012 / f3:+0.029 / f4:+0.008 | 5 |
| hsrl[final] − hsrl[before_stage3] | overall | bal_acc | 5 | 0.007 | 0.011 | -0.007 | 0.021 | 3/5 | f0:-0.005 / f1:-0.000 / f2:+0.005 / f3:+0.024 / f4:+0.010 | 3 |
| hsrl[final] − hsrl[before_stage3] | overall | auroc | 5 | 0.005 | 0.007 | -0.004 | 0.014 | 4/5 | f0:-0.001 / f1:+0.008 / f2:+0.001 / f3:+0.016 / f4:+0.001 | 4 |
| hsrl[final] − hsrl[before_stage3] | unanimous | acc | 5 | 0.006 | 0.011 | -0.008 | 0.020 | 3/5 | f0:-0.003 / f1:+0.000 / f2:+0.003 / f3:+0.026 / f4:+0.003 | 3 |
| hsrl[final] − hsrl[before_stage3] | split_vote | acc | 5 | 0.015 | 0.009 | 0.004 | 0.027 | 5/5 | f0:+0.012 / f1:+0.006 / f2:+0.017 / f3:+0.030 / f4:+0.011 | 5 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | acc | 5 | -0.015 | 0.017 | -0.036 | 0.006 | 0/5 | f0:-0.003 / f1:-0.040 / f2:-0.006 / f3:-0.025 / f4:+0.000 | 4 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | bal_acc | 5 | -0.003 | 0.019 | -0.026 | 0.021 | 2/5 | f0:+0.016 / f1:-0.032 / f2:-0.003 / f3:-0.006 / f4:+0.011 | 3 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | auroc | 5 | -0.010 | 0.009 | -0.021 | 0.001 | 0/5 | f0:-0.002 / f1:-0.020 / f2:-0.009 / f3:-0.000 / f4:-0.017 | 5 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | unanimous | acc | 5 | 0.020 | 0.016 | 0.000 | 0.039 | 5/5 | f0:+0.041 / f1:+0.006 / f2:+0.021 / f3:+0.003 / f4:+0.028 | 5 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | split_vote | acc | 5 | -0.033 | 0.020 | -0.057 | -0.008 | 0/5 | f0:-0.024 / f1:-0.063 / f2:-0.020 / f3:-0.041 / f4:-0.014 | 5 |

### Every run: before (pre) / after (post) Stage III

| run | pre_acc | pre_bal_acc | pre_split_vote_acc | pre_unanimous_acc | post_acc | post_bal_acc | post_split_vote_acc | post_unanimous_acc |
|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.819 | 0.783 | 0.761 | 0.940 | 0.826 | 0.779 | 0.773 | 0.937 |
| f0s0_hsrl_no_stage1 | 0.769 | 0.715 | 0.738 | 0.833 | 0.766 | 0.731 | 0.714 | 0.874 |
| f1s1_hsrl | 0.837 | 0.802 | 0.790 | 0.930 | 0.841 | 0.801 | 0.797 | 0.930 |
| f1s1_hsrl_no_stage1 | 0.781 | 0.726 | 0.760 | 0.823 | 0.741 | 0.694 | 0.697 | 0.829 |
| f2s2_hsrl | 0.818 | 0.808 | 0.763 | 0.927 | 0.830 | 0.813 | 0.780 | 0.930 |
| f2s2_hsrl_no_stage1 | 0.771 | 0.727 | 0.749 | 0.814 | 0.765 | 0.723 | 0.729 | 0.835 |
| f3s3_hsrl | 0.775 | 0.755 | 0.716 | 0.880 | 0.803 | 0.779 | 0.746 | 0.906 |
| f3s3_hsrl_no_stage1 | 0.758 | 0.725 | 0.722 | 0.823 | 0.733 | 0.719 | 0.680 | 0.826 |
| f4s4_hsrl | 0.798 | 0.760 | 0.744 | 0.910 | 0.807 | 0.771 | 0.754 | 0.913 |
| f4s4_hsrl_no_stage1 | 0.754 | 0.684 | 0.730 | 0.804 | 0.754 | 0.696 | 0.716 | 0.832 |

## 4. Stage III pseudo-labels (vs hidden majority labels)

| config | runs | coverage | precision | prec_unanimous | prec_split | min_coverage |
|---|---|---|---|---|---|---|
| hsrl | 5 | 0.698 ± 0.037 | 0.899 ± 0.012 | 0.968 ± 0.008 | 0.855 ± 0.015 | 0.655 |
| hsrl_no_stage1 | 5 | 0.344 ± 0.052 | 0.929 ± 0.012 | 0.975 ± 0.012 | 0.900 ± 0.013 | 0.284 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl | 5 | 30 | 2/5 | 2/5 | 28 23 | 0.143 ± 0.069 | 1.518 ± 0.275 | 0.748 ± 0.026 | 0.22/0.41/0.06 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.937 | 0.236 | 7 | nan | nan | 1.667 | 0.735 |
| f1s1_hsrl | 0.900 | 0.130 | 13 | nan | nan | 1.659 | 0.790 |
| f2s2_hsrl | 0.740 | 0.065 | 20 | 14.000 | 28.000 | 1.033 | 0.719 |
| f3s3_hsrl | 0.944 | 0.189 | 10 | nan | nan | 1.666 | 0.754 |
| f4s4_hsrl | 0.990 | 0.097 | 15 | 14.000 | 23.000 | 1.565 | 0.741 |
