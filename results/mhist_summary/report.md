# Aggregate over results/mhist

Runs: 50; folds [0, 1, 2, 3, 4]; seeds [0, 1, 2, 3, 4]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl | 5 | 0.776 ± 0.022 | 0.752 ± 0.030 | 0.754 ± 0.025 | 0.855 ± 0.025 | 0.169 ± 0.017 | 0.871 ± 0.037 | 0.728 ± 0.031 |
| hsrl_no_stage1 | 5 | 0.737 ± 0.014 | 0.701 ± 0.023 | 0.705 ± 0.021 | 0.805 ± 0.016 | 0.173 ± 0.006 | 0.808 ± 0.023 | 0.702 ± 0.017 |
| hsrl_no_t2 | 5 | 0.786 ± 0.010 | 0.765 ± 0.023 | 0.766 ± 0.017 | 0.859 ± 0.011 | 0.163 ± 0.007 | 0.870 ± 0.034 | 0.745 ± 0.022 |
| hsrl_soft | 5 | 0.770 ± 0.029 | 0.771 ± 0.028 | 0.761 ± 0.029 | 0.858 ± 0.021 | 0.165 ± 0.018 | 0.887 ± 0.035 | 0.713 ± 0.034 |
| hsrl_triplet | 5 | 0.783 ± 0.019 | 0.750 ± 0.022 | 0.757 ± 0.021 | 0.857 ± 0.021 | 0.166 ± 0.017 | 0.863 ± 0.028 | 0.744 ± 0.028 |
| supervised | 5 | 0.767 ± 0.028 | 0.749 ± 0.028 | 0.749 ± 0.027 | 0.842 ± 0.033 | 0.187 ± 0.024 | 0.865 ± 0.032 | 0.719 ± 0.036 |
| supervised_full | 5 | 0.845 ± 0.016 | 0.824 ± 0.020 | 0.830 ± 0.018 | 0.917 ± 0.010 | 0.125 ± 0.013 | 0.921 ± 0.023 | 0.807 ± 0.015 |
| supervised_p20 | 5 | 0.801 ± 0.011 | 0.792 ± 0.014 | 0.788 ± 0.011 | 0.879 ± 0.015 | 0.163 ± 0.012 | 0.906 ± 0.020 | 0.749 ± 0.011 |
| supervised_p50 | 5 | 0.836 ± 0.015 | 0.815 ± 0.020 | 0.821 ± 0.018 | 0.903 ± 0.009 | 0.133 ± 0.010 | 0.924 ± 0.016 | 0.793 ± 0.016 |
| supervised_soft | 5 | 0.781 ± 0.019 | 0.765 ± 0.027 | 0.764 ± 0.023 | 0.854 ± 0.021 | 0.153 ± 0.009 | 0.884 ± 0.036 | 0.729 ± 0.024 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl | 0 | 1 | 0.784 | 0.790 | 0.875 | 0.713 |
| hsrl_no_stage1 | 0 | 1 | 0.735 | 0.710 | 0.811 | 0.699 |
| hsrl_no_t2 | 0 | 1 | 0.781 | 0.786 | 0.868 | 0.711 |
| hsrl_soft | 0 | 1 | 0.779 | 0.792 | 0.876 | 0.705 |
| hsrl_triplet | 0 | 1 | 0.808 | 0.782 | 0.880 | 0.766 |
| supervised | 0 | 1 | 0.787 | 0.782 | 0.873 | 0.728 |
| supervised_full | 0 | 1 | 0.841 | 0.812 | 0.913 | 0.810 |
| supervised_p20 | 0 | 1 | 0.803 | 0.797 | 0.881 | 0.751 |
| supervised_p50 | 0 | 1 | 0.833 | 0.812 | 0.900 | 0.790 |
| supervised_soft | 0 | 1 | 0.766 | 0.770 | 0.859 | 0.693 |
| hsrl | 1 | 1 | 0.802 | 0.777 | 0.878 | 0.761 |
| hsrl_no_stage1 | 1 | 1 | 0.754 | 0.716 | 0.818 | 0.719 |
| hsrl_no_t2 | 1 | 1 | 0.788 | 0.757 | 0.864 | 0.748 |
| hsrl_soft | 1 | 1 | 0.802 | 0.802 | 0.880 | 0.745 |
| hsrl_triplet | 1 | 1 | 0.792 | 0.750 | 0.874 | 0.760 |
| supervised | 1 | 1 | 0.785 | 0.768 | 0.877 | 0.734 |
| supervised_full | 1 | 1 | 0.823 | 0.800 | 0.907 | 0.790 |
| supervised_p20 | 1 | 1 | 0.810 | 0.782 | 0.887 | 0.766 |
| supervised_p50 | 1 | 1 | 0.860 | 0.849 | 0.918 | 0.815 |
| supervised_soft | 1 | 1 | 0.798 | 0.791 | 0.879 | 0.743 |
| hsrl | 2 | 1 | 0.773 | 0.743 | 0.848 | 0.734 |
| hsrl_no_stage1 | 2 | 1 | 0.740 | 0.722 | 0.809 | 0.693 |
| hsrl_no_t2 | 2 | 1 | 0.800 | 0.782 | 0.866 | 0.772 |
| hsrl_soft | 2 | 1 | 0.756 | 0.757 | 0.847 | 0.708 |
| hsrl_triplet | 2 | 1 | 0.787 | 0.748 | 0.852 | 0.751 |
| supervised | 2 | 1 | 0.766 | 0.751 | 0.818 | 0.723 |
| supervised_full | 2 | 1 | 0.859 | 0.834 | 0.927 | 0.820 |
| supervised_p20 | 2 | 1 | 0.805 | 0.805 | 0.896 | 0.749 |
| supervised_p50 | 2 | 1 | 0.841 | 0.814 | 0.905 | 0.803 |
| supervised_soft | 2 | 1 | 0.801 | 0.790 | 0.862 | 0.749 |
| hsrl | 3 | 1 | 0.741 | 0.722 | 0.817 | 0.683 |
| hsrl_no_stage1 | 3 | 1 | 0.716 | 0.667 | 0.777 | 0.682 |
| hsrl_no_t2 | 3 | 1 | 0.788 | 0.770 | 0.857 | 0.748 |
| hsrl_soft | 3 | 1 | 0.727 | 0.731 | 0.828 | 0.662 |
| hsrl_triplet | 3 | 1 | 0.757 | 0.752 | 0.827 | 0.696 |
| supervised | 3 | 1 | 0.721 | 0.711 | 0.800 | 0.657 |
| supervised_full | 3 | 1 | 0.839 | 0.821 | 0.911 | 0.792 |
| supervised_p20 | 3 | 1 | 0.782 | 0.772 | 0.856 | 0.736 |
| supervised_p50 | 3 | 1 | 0.821 | 0.794 | 0.894 | 0.778 |
| supervised_soft | 3 | 1 | 0.760 | 0.738 | 0.824 | 0.717 |
| hsrl | 4 | 1 | 0.778 | 0.730 | 0.857 | 0.751 |
| hsrl_no_stage1 | 4 | 1 | 0.742 | 0.688 | 0.812 | 0.720 |
| hsrl_no_t2 | 4 | 1 | 0.773 | 0.729 | 0.842 | 0.745 |
| hsrl_soft | 4 | 1 | 0.786 | 0.774 | 0.860 | 0.743 |
| hsrl_triplet | 4 | 1 | 0.771 | 0.719 | 0.854 | 0.746 |
| supervised | 4 | 1 | 0.779 | 0.732 | 0.842 | 0.754 |
| supervised_full | 4 | 1 | 0.861 | 0.853 | 0.928 | 0.823 |
| supervised_p20 | 4 | 1 | 0.803 | 0.803 | 0.876 | 0.743 |
| supervised_p50 | 4 | 1 | 0.827 | 0.806 | 0.896 | 0.780 |
| supervised_soft | 4 | 1 | 0.777 | 0.737 | 0.845 | 0.745 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl − supervised | overall | acc | 5 | 0.008 | 0.011 | -0.005 | 0.021 | 3/5 | f0:-0.003 / f1:+0.017 / f2:+0.007 / f3:+0.020 / f4:-0.001 | 3 |
| hsrl − supervised | overall | bal_acc | 5 | 0.004 | 0.008 | -0.007 | 0.014 | 3/5 | f0:+0.008 / f1:+0.009 / f2:-0.008 / f3:+0.012 / f4:-0.001 | 3 |
| hsrl − supervised | overall | auroc | 5 | 0.013 | 0.012 | -0.002 | 0.027 | 5/5 | f0:+0.002 / f1:+0.001 / f2:+0.029 / f3:+0.016 / f4:+0.015 | 5 |
| hsrl − supervised | overall | brier | 5 | -0.018 | 0.008 | -0.028 | -0.009 | 5/5 | f0:-0.009 / f1:-0.015 / f2:-0.024 / f3:-0.028 / f4:-0.015 | 5 |
| hsrl − supervised | split_vote | acc | 5 | 0.009 | 0.019 | -0.014 | 0.032 | 3/5 | f0:-0.015 / f1:+0.028 / f2:+0.011 / f3:+0.026 / f4:-0.003 | 3 |
| hsrl − hsrl_no_stage1 | overall | acc | 5 | 0.038 | 0.010 | 0.026 | 0.051 | 5/5 | f0:+0.049 / f1:+0.048 / f2:+0.033 / f3:+0.025 / f4:+0.036 | 5 |
| hsrl − hsrl_no_stage1 | overall | bal_acc | 5 | 0.052 | 0.022 | 0.024 | 0.079 | 5/5 | f0:+0.079 / f1:+0.061 / f2:+0.020 / f3:+0.055 / f4:+0.043 | 5 |
| hsrl − hsrl_no_stage1 | overall | auroc | 5 | 0.049 | 0.012 | 0.035 | 0.064 | 5/5 | f0:+0.064 / f1:+0.060 / f2:+0.038 / f3:+0.040 / f4:+0.045 | 5 |
| hsrl − hsrl_no_stage1 | overall | brier | 5 | -0.004 | 0.011 | -0.018 | 0.009 | 3/5 | f0:-0.013 / f1:-0.018 / f2:+0.003 / f3:+0.009 / f4:-0.003 | 3 |
| hsrl − hsrl_no_stage1 | split_vote | acc | 5 | 0.026 | 0.018 | 0.004 | 0.048 | 5/5 | f0:+0.014 / f1:+0.043 / f2:+0.041 / f3:+0.001 / f4:+0.031 | 5 |
| hsrl − hsrl_triplet | overall | acc | 5 | -0.007 | 0.015 | -0.026 | 0.011 | 2/5 | f0:-0.024 / f1:+0.010 / f2:-0.014 / f3:-0.016 / f4:+0.007 | 3 |
| hsrl − hsrl_triplet | overall | bal_acc | 5 | 0.002 | 0.021 | -0.024 | 0.029 | 3/5 | f0:+0.007 / f1:+0.027 / f2:-0.005 / f3:-0.030 / f4:+0.011 | 3 |
| hsrl − hsrl_triplet | overall | auroc | 5 | -0.003 | 0.006 | -0.010 | 0.005 | 2/5 | f0:-0.005 / f1:+0.004 / f2:-0.004 / f3:-0.010 / f4:+0.003 | 3 |
| hsrl − hsrl_triplet | overall | brier | 5 | 0.003 | 0.009 | -0.008 | 0.014 | 1/5 | f0:+0.015 / f1:-0.011 / f2:+0.003 / f3:+0.005 / f4:+0.002 | 4 |
| hsrl − hsrl_triplet | split_vote | acc | 5 | -0.015 | 0.023 | -0.044 | 0.014 | 2/5 | f0:-0.054 / f1:+0.002 / f2:-0.017 / f3:-0.012 / f4:+0.005 | 3 |
| hsrl − hsrl_no_t2 | overall | acc | 5 | -0.010 | 0.026 | -0.043 | 0.022 | 3/5 | f0:+0.003 / f1:+0.014 / f2:-0.028 / f3:-0.047 / f4:+0.005 | 2 |
| hsrl − hsrl_no_t2 | overall | bal_acc | 5 | -0.013 | 0.030 | -0.049 | 0.024 | 3/5 | f0:+0.004 / f1:+0.020 / f2:-0.039 / f3:-0.048 / f4:+0.001 | 2 |
| hsrl − hsrl_no_t2 | overall | auroc | 5 | -0.004 | 0.024 | -0.034 | 0.025 | 3/5 | f0:+0.008 / f1:+0.014 / f2:-0.019 / f3:-0.040 / f4:+0.015 | 2 |
| hsrl − hsrl_no_t2 | overall | brier | 5 | 0.006 | 0.019 | -0.017 | 0.029 | 3/5 | f0:-0.007 / f1:-0.011 / f2:+0.023 / f3:+0.029 / f4:-0.005 | 2 |
| hsrl − hsrl_no_t2 | split_vote | acc | 5 | -0.016 | 0.034 | -0.058 | 0.025 | 3/5 | f0:+0.002 / f1:+0.014 / f2:-0.038 / f3:-0.064 / f4:+0.006 | 2 |
| supervised_full − supervised | overall | acc | 5 | 0.077 | 0.032 | 0.038 | 0.117 | 5/5 | f0:+0.054 / f1:+0.038 / f2:+0.093 / f3:+0.119 / f4:+0.082 | 5 |
| supervised_full − supervised | overall | bal_acc | 5 | 0.076 | 0.042 | 0.023 | 0.128 | 5/5 | f0:+0.031 / f1:+0.032 / f2:+0.084 / f3:+0.110 / f4:+0.121 | 5 |
| supervised_full − supervised | overall | auroc | 5 | 0.075 | 0.038 | 0.028 | 0.122 | 5/5 | f0:+0.040 / f1:+0.030 / f2:+0.109 / f3:+0.110 / f4:+0.086 | 5 |
| supervised_full − supervised | overall | brier | 5 | -0.062 | 0.030 | -0.099 | -0.024 | 5/5 | f0:-0.037 / f1:-0.023 / f2:-0.089 / f3:-0.088 / f4:-0.071 | 5 |
| supervised_full − supervised | split_vote | acc | 5 | 0.088 | 0.030 | 0.050 | 0.125 | 5/5 | f0:+0.083 / f1:+0.057 / f2:+0.096 / f3:+0.135 / f4:+0.069 | 5 |
| supervised_full − hsrl | overall | acc | 5 | 0.069 | 0.031 | 0.031 | 0.107 | 5/5 | f0:+0.057 / f1:+0.020 / f2:+0.086 / f3:+0.098 / f4:+0.083 | 5 |
| supervised_full − hsrl | overall | bal_acc | 5 | 0.072 | 0.046 | 0.015 | 0.129 | 5/5 | f0:+0.023 / f1:+0.023 / f2:+0.092 / f3:+0.099 / f4:+0.122 | 5 |
| supervised_full − hsrl | overall | auroc | 5 | 0.062 | 0.028 | 0.028 | 0.097 | 5/5 | f0:+0.038 / f1:+0.029 / f2:+0.080 / f3:+0.094 / f4:+0.071 | 5 |
| supervised_full − hsrl | overall | brier | 5 | -0.043 | 0.024 | -0.074 | -0.013 | 5/5 | f0:-0.028 / f1:-0.008 / f2:-0.065 / f3:-0.060 / f4:-0.056 | 5 |
| supervised_full − hsrl | split_vote | acc | 5 | 0.079 | 0.031 | 0.040 | 0.117 | 5/5 | f0:+0.098 / f1:+0.029 / f2:+0.086 / f3:+0.109 / f4:+0.072 | 5 |
| supervised_p20 − supervised | overall | acc | 5 | 0.033 | 0.018 | 0.011 | 0.056 | 5/5 | f0:+0.016 / f1:+0.024 / f2:+0.040 / f3:+0.061 / f4:+0.025 | 5 |
| supervised_p20 − supervised | overall | bal_acc | 5 | 0.043 | 0.027 | 0.010 | 0.077 | 5/5 | f0:+0.016 / f1:+0.014 / f2:+0.054 / f3:+0.062 / f4:+0.071 | 5 |
| supervised_p20 − supervised | overall | auroc | 5 | 0.037 | 0.030 | 0.000 | 0.074 | 5/5 | f0:+0.009 / f1:+0.010 / f2:+0.078 / f3:+0.055 / f4:+0.034 | 5 |
| supervised_p20 − supervised | overall | brier | 5 | -0.024 | 0.018 | -0.047 | -0.002 | 5/5 | f0:-0.006 / f1:-0.009 / f2:-0.048 / f3:-0.038 / f4:-0.021 | 5 |
| supervised_p20 − supervised | split_vote | acc | 5 | 0.030 | 0.032 | -0.010 | 0.069 | 4/5 | f0:+0.023 / f1:+0.032 / f2:+0.026 / f3:+0.078 / f4:-0.011 | 4 |
| supervised_p50 − supervised | overall | acc | 5 | 0.069 | 0.022 | 0.041 | 0.097 | 5/5 | f0:+0.046 / f1:+0.075 / f2:+0.076 / f3:+0.100 / f4:+0.048 | 5 |
| supervised_p50 − supervised | overall | bal_acc | 5 | 0.067 | 0.022 | 0.039 | 0.094 | 5/5 | f0:+0.030 / f1:+0.081 / f2:+0.063 / f3:+0.084 / f4:+0.074 | 5 |
| supervised_p50 − supervised | overall | auroc | 5 | 0.061 | 0.029 | 0.025 | 0.096 | 5/5 | f0:+0.027 / f1:+0.041 / f2:+0.087 / f3:+0.094 / f4:+0.055 | 5 |
| supervised_p50 − supervised | overall | brier | 5 | -0.054 | 0.021 | -0.080 | -0.028 | 5/5 | f0:-0.029 / f1:-0.047 / f2:-0.070 / f3:-0.080 / f4:-0.042 | 5 |
| supervised_p50 − supervised | split_vote | acc | 5 | 0.074 | 0.034 | 0.031 | 0.117 | 5/5 | f0:+0.063 / f1:+0.081 / f2:+0.080 / f3:+0.121 / f4:+0.026 | 5 |
| supervised_soft − supervised | overall | acc | 5 | 0.013 | 0.026 | -0.019 | 0.045 | 3/5 | f0:-0.022 / f1:+0.013 / f2:+0.036 / f3:+0.040 / f4:-0.002 | 3 |
| supervised_soft − supervised | overall | bal_acc | 5 | 0.017 | 0.020 | -0.008 | 0.041 | 4/5 | f0:-0.012 / f1:+0.023 / f2:+0.039 / f3:+0.027 / f4:+0.005 | 4 |
| supervised_soft − supervised | overall | auroc | 5 | 0.012 | 0.022 | -0.016 | 0.039 | 4/5 | f0:-0.014 / f1:+0.002 / f2:+0.044 / f3:+0.023 / f4:+0.004 | 4 |
| supervised_soft − supervised | overall | brier | 5 | -0.034 | 0.019 | -0.057 | -0.010 | 5/5 | f0:-0.012 / f1:-0.022 / f2:-0.051 / f3:-0.055 / f4:-0.027 | 5 |
| supervised_soft − supervised | split_vote | acc | 5 | 0.010 | 0.036 | -0.034 | 0.055 | 3/5 | f0:-0.035 / f1:+0.009 / f2:+0.026 / f3:+0.060 / f4:-0.009 | 3 |
| hsrl_soft − hsrl | overall | acc | 5 | -0.006 | 0.010 | -0.018 | 0.007 | 1/5 | f0:-0.005 / f1:+0.000 / f2:-0.016 / f3:-0.014 / f4:+0.008 | 3 |
| hsrl_soft − hsrl | overall | bal_acc | 5 | 0.019 | 0.016 | -0.001 | 0.039 | 5/5 | f0:+0.002 / f1:+0.025 / f2:+0.015 / f3:+0.009 / f4:+0.044 | 5 |
| hsrl_soft − hsrl | overall | auroc | 5 | 0.003 | 0.005 | -0.003 | 0.009 | 4/5 | f0:+0.000 / f1:+0.002 / f2:-0.001 / f3:+0.011 / f4:+0.003 | 4 |
| hsrl_soft − hsrl | overall | brier | 5 | -0.004 | 0.008 | -0.014 | 0.005 | 4/5 | f0:-0.004 / f1:-0.002 / f2:+0.005 / f3:-0.004 / f4:-0.016 | 4 |
| hsrl_soft − hsrl | split_vote | acc | 5 | -0.016 | 0.008 | -0.026 | -0.006 | 0/5 | f0:-0.008 / f1:-0.017 / f2:-0.026 / f3:-0.021 / f4:-0.008 | 5 |
| hsrl_soft − supervised_soft | overall | acc | 5 | -0.010 | 0.027 | -0.044 | 0.023 | 3/5 | f0:+0.013 / f1:+0.004 / f2:-0.045 / f3:-0.034 / f4:+0.009 | 2 |
| hsrl_soft − supervised_soft | overall | bal_acc | 5 | 0.006 | 0.027 | -0.027 | 0.040 | 3/5 | f0:+0.022 / f1:+0.011 / f2:-0.033 / f3:-0.007 / f4:+0.038 | 3 |
| hsrl_soft − supervised_soft | overall | auroc | 5 | 0.004 | 0.013 | -0.012 | 0.020 | 4/5 | f0:+0.017 / f1:+0.001 / f2:-0.015 / f3:+0.004 / f4:+0.014 | 4 |
| hsrl_soft − supervised_soft | overall | brier | 5 | 0.011 | 0.016 | -0.008 | 0.030 | 2/5 | f0:-0.001 / f1:+0.006 / f2:+0.032 / f3:+0.023 / f4:-0.004 | 3 |
| hsrl_soft − supervised_soft | split_vote | acc | 5 | -0.017 | 0.029 | -0.053 | 0.020 | 2/5 | f0:+0.012 / f1:+0.002 / f2:-0.041 / f3:-0.055 / f4:-0.002 | 3 |

## 3. Effect of Stage III (after − before, paired within run)

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl[final] − hsrl[before_stage3] | overall | acc | 5 | 0.010 | 0.008 | 0.000 | 0.020 | 4/5 | f0:+0.020 / f1:+0.012 / f2:+0.013 / f3:+0.004 / f4:+0.000 | 4 |
| hsrl[final] − hsrl[before_stage3] | overall | bal_acc | 5 | 0.005 | 0.011 | -0.009 | 0.019 | 4/5 | f0:+0.021 / f1:+0.006 / f2:+0.008 / f3:+0.002 / f4:-0.010 | 4 |
| hsrl[final] − hsrl[before_stage3] | overall | auroc | 5 | 0.012 | 0.007 | 0.004 | 0.020 | 5/5 | f0:+0.021 / f1:+0.011 / f2:+0.008 / f3:+0.015 / f4:+0.004 | 5 |
| hsrl[final] − hsrl[before_stage3] | unanimous | acc | 5 | 0.007 | 0.011 | -0.007 | 0.021 | 3/5 | f0:+0.022 / f1:+0.003 / f2:+0.016 / f3:+0.000 / f4:-0.006 | 3 |
| hsrl[final] − hsrl[before_stage3] | split_vote | acc | 5 | 0.012 | 0.007 | 0.003 | 0.020 | 5/5 | f0:+0.020 / f1:+0.017 / f2:+0.012 / f3:+0.006 / f4:+0.003 | 5 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | acc | 5 | -0.021 | 0.011 | -0.035 | -0.008 | 0/5 | f0:-0.012 / f1:-0.011 / f2:-0.027 / f3:-0.037 / f4:-0.019 | 5 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | bal_acc | 5 | -0.018 | 0.010 | -0.030 | -0.005 | 0/5 | f0:-0.010 / f1:-0.008 / f2:-0.014 / f3:-0.030 / f4:-0.027 | 5 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | auroc | 5 | -0.027 | 0.017 | -0.048 | -0.006 | 0/5 | f0:-0.010 / f1:-0.024 / f2:-0.016 / f3:-0.053 / f4:-0.031 | 5 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | unanimous | acc | 5 | 0.001 | 0.017 | -0.020 | 0.022 | 2/5 | f0:+0.012 / f1:+0.025 / f2:-0.003 / f3:-0.012 / f4:-0.015 | 2 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | split_vote | acc | 5 | -0.032 | 0.011 | -0.046 | -0.018 | 0/5 | f0:-0.024 / f1:-0.029 / f2:-0.038 / f3:-0.049 / f4:-0.021 | 5 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | overall | acc | 5 | 0.018 | 0.012 | 0.003 | 0.033 | 5/5 | f0:+0.013 / f1:+0.010 / f2:+0.035 / f3:+0.027 / f4:+0.006 | 5 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | overall | bal_acc | 5 | 0.017 | 0.013 | 0.001 | 0.033 | 5/5 | f0:+0.014 / f1:+0.008 / f2:+0.032 / f3:+0.027 / f4:+0.003 | 5 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | overall | auroc | 5 | 0.015 | 0.009 | 0.004 | 0.026 | 5/5 | f0:+0.014 / f1:+0.007 / f2:+0.020 / f3:+0.028 / f4:+0.006 | 5 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | unanimous | acc | 5 | 0.015 | 0.009 | 0.004 | 0.026 | 4/5 | f0:+0.015 / f1:+0.015 / f2:+0.019 / f3:+0.025 / f4:+0.000 | 4 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | split_vote | acc | 5 | 0.020 | 0.015 | 0.001 | 0.039 | 5/5 | f0:+0.012 / f1:+0.008 / f2:+0.043 / f3:+0.028 / f4:+0.009 | 5 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | acc | 5 | 0.003 | 0.010 | -0.010 | 0.016 | 2/5 | f0:-0.001 / f1:+0.011 / f2:-0.009 / f3:-0.002 / f4:+0.016 | 2 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | bal_acc | 5 | 0.023 | 0.016 | 0.003 | 0.043 | 5/5 | f0:+0.003 / f1:+0.037 / f2:+0.016 / f3:+0.017 / f4:+0.041 | 5 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | auroc | 5 | 0.019 | 0.007 | 0.010 | 0.028 | 5/5 | f0:+0.013 / f1:+0.020 / f2:+0.012 / f3:+0.030 / f4:+0.020 | 5 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | unanimous | acc | 5 | 0.017 | 0.012 | 0.002 | 0.033 | 5/5 | f0:+0.015 / f1:+0.034 / f2:+0.009 / f3:+0.003 / f4:+0.025 | 5 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | split_vote | acc | 5 | -0.004 | 0.011 | -0.018 | 0.010 | 1/5 | f0:-0.009 / f1:+0.000 / f2:-0.018 / f3:-0.005 / f4:+0.012 | 3 |
| hsrl_triplet[final] − hsrl_triplet[before_stage3] | overall | acc | 5 | 0.011 | 0.012 | -0.004 | 0.027 | 4/5 | f0:+0.001 / f1:+0.018 / f2:+0.026 / f3:+0.016 / f4:-0.004 | 4 |
| hsrl_triplet[final] − hsrl_triplet[before_stage3] | overall | bal_acc | 5 | 0.002 | 0.013 | -0.014 | 0.018 | 3/5 | f0:-0.007 / f1:+0.007 / f2:+0.006 / f3:+0.018 / f4:-0.015 | 3 |
| hsrl_triplet[final] − hsrl_triplet[before_stage3] | overall | auroc | 5 | 0.011 | 0.008 | 0.002 | 0.021 | 5/5 | f0:+0.007 / f1:+0.013 / f2:+0.013 / f3:+0.022 / f4:+0.002 | 5 |
| hsrl_triplet[final] − hsrl_triplet[before_stage3] | unanimous | acc | 5 | -0.000 | 0.023 | -0.028 | 0.028 | 2/5 | f0:-0.016 / f1:+0.000 / f2:+0.006 / f3:+0.034 / f4:-0.025 | 2 |
| hsrl_triplet[final] − hsrl_triplet[before_stage3] | split_vote | acc | 5 | 0.017 | 0.013 | 0.001 | 0.034 | 5/5 | f0:+0.009 / f1:+0.027 / f2:+0.035 / f3:+0.008 / f4:+0.006 | 5 |

### Every run: before (pre) / after (post) Stage III

| run | pre_acc | pre_bal_acc | pre_split_vote_acc | pre_unanimous_acc | post_acc | post_bal_acc | post_split_vote_acc | post_unanimous_acc |
|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.764 | 0.769 | 0.693 | 0.907 | 0.784 | 0.790 | 0.713 | 0.929 |
| f0s0_hsrl_no_stage1 | 0.747 | 0.720 | 0.723 | 0.796 | 0.735 | 0.710 | 0.699 | 0.808 |
| f0s0_hsrl_no_t2 | 0.768 | 0.772 | 0.699 | 0.907 | 0.781 | 0.786 | 0.711 | 0.923 |
| f0s0_hsrl_soft | 0.780 | 0.789 | 0.714 | 0.913 | 0.779 | 0.792 | 0.705 | 0.929 |
| f0s0_hsrl_triplet | 0.807 | 0.789 | 0.757 | 0.907 | 0.808 | 0.782 | 0.766 | 0.892 |
| f1s1_hsrl | 0.790 | 0.771 | 0.745 | 0.882 | 0.802 | 0.777 | 0.761 | 0.885 |
| f1s1_hsrl_no_stage1 | 0.766 | 0.724 | 0.748 | 0.802 | 0.754 | 0.716 | 0.719 | 0.827 |
| f1s1_hsrl_no_t2 | 0.778 | 0.749 | 0.740 | 0.855 | 0.788 | 0.757 | 0.748 | 0.870 |
| f1s1_hsrl_soft | 0.791 | 0.766 | 0.745 | 0.885 | 0.802 | 0.802 | 0.745 | 0.919 |
| f1s1_hsrl_triplet | 0.774 | 0.743 | 0.732 | 0.858 | 0.792 | 0.750 | 0.760 | 0.858 |
| f2s2_hsrl | 0.759 | 0.734 | 0.722 | 0.836 | 0.773 | 0.743 | 0.734 | 0.851 |
| f2s2_hsrl_no_stage1 | 0.767 | 0.736 | 0.731 | 0.839 | 0.740 | 0.722 | 0.693 | 0.836 |
| f2s2_hsrl_no_t2 | 0.766 | 0.750 | 0.729 | 0.839 | 0.800 | 0.782 | 0.772 | 0.858 |
| f2s2_hsrl_soft | 0.766 | 0.742 | 0.726 | 0.845 | 0.756 | 0.757 | 0.708 | 0.855 |
| f2s2_hsrl_triplet | 0.761 | 0.742 | 0.716 | 0.855 | 0.787 | 0.748 | 0.751 | 0.861 |
| f3s3_hsrl | 0.737 | 0.720 | 0.677 | 0.858 | 0.741 | 0.722 | 0.683 | 0.858 |
| f3s3_hsrl_no_stage1 | 0.752 | 0.697 | 0.731 | 0.796 | 0.716 | 0.667 | 0.682 | 0.783 |
| f3s3_hsrl_no_t2 | 0.761 | 0.743 | 0.720 | 0.845 | 0.788 | 0.770 | 0.748 | 0.870 |
| f3s3_hsrl_soft | 0.729 | 0.714 | 0.667 | 0.855 | 0.727 | 0.731 | 0.662 | 0.858 |
| f3s3_hsrl_triplet | 0.741 | 0.734 | 0.688 | 0.848 | 0.757 | 0.752 | 0.696 | 0.882 |
| f4s4_hsrl | 0.778 | 0.741 | 0.748 | 0.839 | 0.778 | 0.730 | 0.751 | 0.833 |
| f4s4_hsrl_no_stage1 | 0.761 | 0.715 | 0.742 | 0.802 | 0.742 | 0.688 | 0.720 | 0.786 |
| f4s4_hsrl_no_t2 | 0.767 | 0.727 | 0.736 | 0.830 | 0.773 | 0.729 | 0.745 | 0.830 |
| f4s4_hsrl_soft | 0.770 | 0.733 | 0.731 | 0.848 | 0.786 | 0.774 | 0.743 | 0.873 |
| f4s4_hsrl_triplet | 0.775 | 0.734 | 0.740 | 0.845 | 0.771 | 0.719 | 0.746 | 0.820 |

## 4. Stage III pseudo-labels (vs hidden majority labels)

| config | runs | coverage | precision | prec_unanimous | prec_split | min_coverage |
|---|---|---|---|---|---|---|
| hsrl | 5 | 0.703 ± 0.022 | 0.911 ± 0.006 | 0.978 ± 0.009 | 0.867 ± 0.010 | 0.678 |
| hsrl_no_stage1 | 5 | 0.364 ± 0.045 | 0.928 ± 0.012 | 0.981 ± 0.006 | 0.895 ± 0.016 | 0.293 |
| hsrl_no_t2 | 5 | 0.724 ± 0.027 | 0.908 ± 0.012 | 0.974 ± 0.009 | 0.866 ± 0.013 | 0.681 |
| hsrl_soft | 5 | 0.299 ± 0.041 | 0.977 ± 0.006 | 0.996 ± 0.005 | 0.959 ± 0.010 | 0.266 |
| hsrl_triplet | 5 | 0.734 ± 0.030 | 0.906 ± 0.004 | 0.971 ± 0.003 | 0.864 ± 0.008 | 0.696 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl | 5 | 30 | 1/5 | 1/5 | 29 | 0.146 ± 0.043 | 1.453 ± 0.388 | 0.764 ± 0.065 | 0.28/0.43/0.06 |
| hsrl_no_t2 | 5 | 30 | 0/5 | 0/5 | - | 0.176 ± 0.042 | 1.643 ± 0.160 | 0.771 ± 0.034 | 0.07/0.52/0.01 |
| hsrl_soft | 5 | 30 | 1/5 | 1/5 | 29 | 0.146 ± 0.043 | 1.453 ± 0.388 | 0.764 ± 0.065 | 0.28/0.43/0.06 |
| hsrl_triplet | 5 | 30 | 1/5 | 1/5 | 26 | 0.113 ± 0.024 | 1.670 ± 0.111 | 0.760 ± 0.037 | 0.19/0.43/0.05 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.903 | 0.196 | 8 | nan | nan | 1.697 | 0.826 |
| f0s0_hsrl_no_t2 | 0.903 | 0.203 | 6 | nan | nan | 1.824 | 0.784 |
| f0s0_hsrl_soft | 0.903 | 0.196 | 8 | nan | nan | 1.697 | 0.826 |
| f0s0_hsrl_triplet | 0.903 | 0.134 | 10 | nan | nan | 1.703 | 0.796 |
| f1s1_hsrl | 0.882 | 0.170 | 11 | nan | nan | 1.773 | 0.832 |
| f1s1_hsrl_no_t2 | 0.882 | 0.197 | 7 | nan | nan | 1.781 | 0.822 |
| f1s1_hsrl_soft | 0.882 | 0.170 | 11 | nan | nan | 1.773 | 0.832 |
| f1s1_hsrl_triplet | 0.882 | 0.131 | 11 | nan | nan | 1.723 | 0.783 |
| f2s2_hsrl | 0.768 | 0.131 | 9 | nan | nan | 1.503 | 0.681 |
| f2s2_hsrl_no_t2 | 0.768 | 0.161 | 6 | nan | nan | 1.538 | 0.747 |
| f2s2_hsrl_soft | 0.768 | 0.131 | 9 | nan | nan | 1.503 | 0.681 |
| f2s2_hsrl_triplet | 0.768 | 0.109 | 9 | nan | nan | 1.603 | 0.700 |
| f3s3_hsrl | 0.946 | 0.081 | 19 | 13.000 | 29.000 | 0.792 | 0.724 |
| f3s3_hsrl_no_t2 | 0.946 | 0.109 | 12 | nan | nan | 1.445 | 0.736 |
| f3s3_hsrl_soft | 0.946 | 0.081 | 19 | 13.000 | 29.000 | 0.792 | 0.724 |
| f3s3_hsrl_triplet | 0.946 | 0.075 | 17 | 10.000 | 26.000 | 1.804 | 0.770 |
| f4s4_hsrl | 0.998 | 0.153 | 12 | nan | nan | 1.500 | 0.756 |
| f4s4_hsrl_no_t2 | 0.998 | 0.209 | 7 | nan | nan | 1.629 | 0.766 |
| f4s4_hsrl_soft | 0.998 | 0.153 | 12 | nan | nan | 1.500 | 0.756 |
| f4s4_hsrl_triplet | 0.998 | 0.118 | 12 | nan | nan | 1.519 | 0.753 |
