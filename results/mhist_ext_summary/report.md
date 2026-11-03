# Aggregate over results/mhist, results/mhist_ext

Runs: 40; folds [0, 1, 2, 3, 4]; seeds [0, 1, 2, 3, 4]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl_soft | 5 | 0.770 ± 0.029 | 0.771 ± 0.028 | 0.761 ± 0.029 | 0.858 ± 0.021 | 0.165 ± 0.018 | 0.887 ± 0.035 | 0.713 ± 0.034 |
| supervised_soft | 5 | 0.781 ± 0.019 | 0.765 ± 0.027 | 0.764 ± 0.023 | 0.854 ± 0.021 | 0.153 ± 0.009 | 0.884 ± 0.036 | 0.729 ± 0.024 |
| interval | 5 | 0.786 ± 0.010 | 0.780 ± 0.012 | 0.774 ± 0.009 | 0.867 ± 0.012 | 0.155 ± 0.009 | 0.898 ± 0.019 | 0.731 ± 0.019 |
| joint | 5 | 0.779 ± 0.023 | 0.773 ± 0.021 | 0.767 ± 0.022 | 0.860 ± 0.018 | 0.162 ± 0.017 | 0.893 ± 0.019 | 0.722 ± 0.036 |
| supported | 5 | 0.781 ± 0.020 | 0.776 ± 0.022 | 0.769 ± 0.021 | 0.861 ± 0.016 | 0.158 ± 0.014 | 0.894 ± 0.028 | 0.726 ± 0.024 |
| supported_conf | 5 | 0.788 ± 0.015 | 0.787 ± 0.014 | 0.778 ± 0.014 | 0.865 ± 0.013 | 0.156 ± 0.013 | 0.893 ± 0.022 | 0.736 ± 0.022 |
| supported_random | 5 | 0.772 ± 0.022 | 0.770 ± 0.023 | 0.761 ± 0.022 | 0.858 ± 0.025 | 0.159 ± 0.017 | 0.887 ± 0.026 | 0.716 ± 0.027 |
| worstcase | 5 | 0.783 ± 0.013 | 0.775 ± 0.020 | 0.770 ± 0.015 | 0.865 ± 0.011 | 0.156 ± 0.008 | 0.889 ± 0.019 | 0.731 ± 0.023 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl_soft | 0 | 1 | 0.779 | 0.792 | 0.876 | 0.705 |
| supervised_soft | 0 | 1 | 0.766 | 0.770 | 0.859 | 0.693 |
| hsrl_soft | 1 | 1 | 0.802 | 0.802 | 0.880 | 0.745 |
| supervised_soft | 1 | 1 | 0.798 | 0.791 | 0.879 | 0.743 |
| hsrl_soft | 2 | 1 | 0.756 | 0.757 | 0.847 | 0.708 |
| supervised_soft | 2 | 1 | 0.801 | 0.790 | 0.862 | 0.749 |
| hsrl_soft | 3 | 1 | 0.727 | 0.731 | 0.828 | 0.662 |
| supervised_soft | 3 | 1 | 0.760 | 0.738 | 0.824 | 0.717 |
| hsrl_soft | 4 | 1 | 0.786 | 0.774 | 0.860 | 0.743 |
| supervised_soft | 4 | 1 | 0.777 | 0.737 | 0.845 | 0.745 |
| interval | 0 | 1 | 0.778 | 0.791 | 0.875 | 0.705 |
| joint | 0 | 1 | 0.764 | 0.778 | 0.860 | 0.690 |
| supported | 0 | 1 | 0.775 | 0.790 | 0.868 | 0.702 |
| supported_conf | 0 | 1 | 0.796 | 0.805 | 0.872 | 0.736 |
| supported_random | 0 | 1 | 0.774 | 0.789 | 0.875 | 0.705 |
| worstcase | 0 | 1 | 0.784 | 0.795 | 0.863 | 0.717 |
| interval | 1 | 1 | 0.800 | 0.788 | 0.878 | 0.749 |
| joint | 1 | 1 | 0.805 | 0.790 | 0.881 | 0.755 |
| supported | 1 | 1 | 0.813 | 0.804 | 0.882 | 0.757 |
| supported_conf | 1 | 1 | 0.802 | 0.796 | 0.880 | 0.751 |
| supported_random | 1 | 1 | 0.795 | 0.790 | 0.880 | 0.736 |
| worstcase | 1 | 1 | 0.785 | 0.788 | 0.880 | 0.734 |
| interval | 2 | 1 | 0.784 | 0.786 | 0.868 | 0.728 |
| joint | 2 | 1 | 0.783 | 0.786 | 0.867 | 0.728 |
| supported | 2 | 1 | 0.783 | 0.777 | 0.862 | 0.736 |
| supported_conf | 2 | 1 | 0.792 | 0.786 | 0.870 | 0.749 |
| supported_random | 2 | 1 | 0.773 | 0.769 | 0.851 | 0.728 |
| worstcase | 2 | 1 | 0.783 | 0.773 | 0.867 | 0.731 |
| interval | 3 | 1 | 0.776 | 0.763 | 0.848 | 0.722 |
| joint | 3 | 1 | 0.747 | 0.736 | 0.830 | 0.680 |
| supported | 3 | 1 | 0.758 | 0.748 | 0.840 | 0.700 |
| supported_conf | 3 | 1 | 0.762 | 0.774 | 0.848 | 0.697 |
| supported_random | 3 | 1 | 0.736 | 0.733 | 0.817 | 0.673 |
| worstcase | 3 | 1 | 0.762 | 0.743 | 0.850 | 0.706 |
| interval | 4 | 1 | 0.792 | 0.772 | 0.868 | 0.751 |
| joint | 4 | 1 | 0.794 | 0.775 | 0.862 | 0.758 |
| supported | 4 | 1 | 0.778 | 0.762 | 0.854 | 0.734 |
| supported_conf | 4 | 1 | 0.785 | 0.773 | 0.858 | 0.746 |
| supported_random | 4 | 1 | 0.784 | 0.768 | 0.865 | 0.739 |
| worstcase | 4 | 1 | 0.800 | 0.777 | 0.868 | 0.766 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| supported − hsrl_soft | overall | acc | 5 | 0.011 | 0.018 | -0.011 | 0.033 | 3/5 | f0:-0.004 / f1:+0.010 / f2:+0.027 / f3:+0.032 / f4:-0.008 | 3 |
| supported − hsrl_soft | overall | bal_acc | 5 | 0.005 | 0.014 | -0.012 | 0.022 | 3/5 | f0:-0.002 / f1:+0.001 / f2:+0.020 / f3:+0.017 / f4:-0.013 | 3 |
| supported − hsrl_soft | overall | auroc | 5 | 0.003 | 0.010 | -0.010 | 0.016 | 3/5 | f0:-0.007 / f1:+0.002 / f2:+0.015 / f3:+0.011 / f4:-0.006 | 3 |
| supported − hsrl_soft | overall | brier | 5 | -0.006 | 0.014 | -0.024 | 0.011 | 3/5 | f0:+0.015 / f1:-0.010 / f2:-0.020 / f3:-0.016 / f4:+0.000 | 3 |
| supported − hsrl_soft | split_vote | acc | 5 | 0.013 | 0.020 | -0.012 | 0.038 | 3/5 | f0:-0.003 / f1:+0.012 / f2:+0.028 / f3:+0.038 / f4:-0.009 | 3 |
| supported_random − hsrl_soft | overall | acc | 5 | 0.002 | 0.010 | -0.010 | 0.015 | 2/5 | f0:-0.005 / f1:-0.007 / f2:+0.016 / f3:+0.009 / f4:-0.002 | 2 |
| supported_random − hsrl_soft | overall | bal_acc | 5 | -0.002 | 0.009 | -0.013 | 0.009 | 2/5 | f0:-0.003 / f1:-0.012 / f2:+0.011 / f3:+0.002 / f4:-0.007 | 3 |
| supported_random − hsrl_soft | overall | auroc | 5 | -0.001 | 0.006 | -0.009 | 0.007 | 2/5 | f0:-0.000 / f1:-0.000 / f2:+0.004 / f3:-0.011 / f4:+0.005 | 3 |
| supported_random − hsrl_soft | overall | brier | 5 | -0.006 | 0.004 | -0.010 | -0.001 | 4/5 | f0:+0.001 / f1:-0.006 / f2:-0.010 / f3:-0.006 / f4:-0.006 | 4 |
| supported_random − hsrl_soft | split_vote | acc | 5 | 0.003 | 0.012 | -0.011 | 0.018 | 2/5 | f0:+0.000 / f1:-0.009 / f2:+0.020 / f3:+0.011 / f4:-0.005 | 2 |
| supported_conf − hsrl_soft | overall | acc | 5 | 0.018 | 0.018 | -0.005 | 0.040 | 3/5 | f0:+0.017 / f1:+0.000 / f2:+0.036 / f3:+0.036 / f4:-0.001 | 3 |
| supported_conf − hsrl_soft | overall | bal_acc | 5 | 0.015 | 0.021 | -0.010 | 0.041 | 3/5 | f0:+0.013 / f1:-0.007 / f2:+0.029 / f3:+0.043 / f4:-0.001 | 3 |
| supported_conf − hsrl_soft | overall | auroc | 5 | 0.007 | 0.013 | -0.009 | 0.023 | 2/5 | f0:-0.004 / f1:-0.000 / f2:+0.023 / f3:+0.019 / f4:-0.002 | 2 |
| supported_conf − hsrl_soft | overall | brier | 5 | -0.009 | 0.012 | -0.023 | 0.005 | 4/5 | f0:+0.003 / f1:-0.007 / f2:-0.027 / f3:-0.011 / f4:-0.002 | 4 |
| supported_conf − hsrl_soft | split_vote | acc | 5 | 0.023 | 0.017 | 0.002 | 0.045 | 5/5 | f0:+0.031 / f1:+0.006 / f2:+0.041 / f3:+0.035 / f4:+0.003 | 5 |
| interval − hsrl_soft | overall | acc | 5 | 0.016 | 0.022 | -0.011 | 0.043 | 3/5 | f0:-0.001 / f1:-0.002 / f2:+0.028 / f3:+0.049 / f4:+0.006 | 3 |
| interval − hsrl_soft | overall | bal_acc | 5 | 0.009 | 0.021 | -0.017 | 0.034 | 2/5 | f0:-0.001 / f1:-0.014 / f2:+0.028 / f3:+0.032 / f4:-0.003 | 2 |
| interval − hsrl_soft | overall | auroc | 5 | 0.009 | 0.011 | -0.005 | 0.023 | 3/5 | f0:-0.001 / f1:-0.002 / f2:+0.021 / f3:+0.020 / f4:+0.008 | 3 |
| interval − hsrl_soft | overall | brier | 5 | -0.010 | 0.012 | -0.025 | 0.005 | 4/5 | f0:+0.005 / f1:-0.003 / f2:-0.022 / f3:-0.022 / f4:-0.007 | 4 |
| interval − hsrl_soft | split_vote | acc | 5 | 0.018 | 0.024 | -0.012 | 0.048 | 4/5 | f0:+0.000 / f1:+0.005 / f2:+0.020 / f3:+0.060 / f4:+0.008 | 4 |
| worstcase − hsrl_soft | overall | acc | 5 | 0.013 | 0.021 | -0.013 | 0.038 | 4/5 | f0:+0.005 / f1:-0.017 / f2:+0.027 / f3:+0.036 / f4:+0.014 | 4 |
| worstcase − hsrl_soft | overall | bal_acc | 5 | 0.004 | 0.012 | -0.011 | 0.018 | 4/5 | f0:+0.003 / f1:-0.015 / f2:+0.016 / f3:+0.012 / f4:+0.003 | 4 |
| worstcase − hsrl_soft | overall | auroc | 5 | 0.007 | 0.014 | -0.010 | 0.025 | 4/5 | f0:-0.013 / f1:+0.000 / f2:+0.020 / f3:+0.021 / f4:+0.008 | 4 |
| worstcase − hsrl_soft | overall | brier | 5 | -0.009 | 0.015 | -0.027 | 0.010 | 3/5 | f0:+0.008 / f1:+0.005 / f2:-0.024 / f3:-0.023 / f4:-0.008 | 3 |
| worstcase − hsrl_soft | split_vote | acc | 5 | 0.018 | 0.020 | -0.006 | 0.043 | 4/5 | f0:+0.012 / f1:-0.011 / f2:+0.023 / f3:+0.044 / f4:+0.023 | 4 |
| joint − hsrl_soft | overall | acc | 5 | 0.009 | 0.016 | -0.012 | 0.029 | 4/5 | f0:-0.015 / f1:+0.003 / f2:+0.027 / f3:+0.020 / f4:+0.008 | 4 |
| joint − hsrl_soft | overall | bal_acc | 5 | 0.001 | 0.017 | -0.020 | 0.023 | 3/5 | f0:-0.014 / f1:-0.013 / f2:+0.029 / f3:+0.005 / f4:+0.000 | 3 |
| joint − hsrl_soft | overall | auroc | 5 | 0.002 | 0.013 | -0.014 | 0.018 | 4/5 | f0:-0.016 / f1:+0.001 / f2:+0.020 / f3:+0.002 / f4:+0.002 | 4 |
| joint − hsrl_soft | overall | brier | 5 | -0.002 | 0.013 | -0.019 | 0.014 | 4/5 | f0:+0.019 / f1:-0.005 / f2:-0.019 / f3:-0.004 / f4:-0.004 | 4 |
| joint − hsrl_soft | split_vote | acc | 5 | 0.010 | 0.014 | -0.008 | 0.028 | 4/5 | f0:-0.015 / f1:+0.011 / f2:+0.020 / f3:+0.018 / f4:+0.015 | 4 |
| supported − supported_random | overall | acc | 5 | 0.009 | 0.012 | -0.006 | 0.024 | 4/5 | f0:+0.001 / f1:+0.017 / f2:+0.010 / f3:+0.022 / f4:-0.006 | 4 |
| supported − supported_random | overall | bal_acc | 5 | 0.007 | 0.009 | -0.004 | 0.018 | 4/5 | f0:+0.001 / f1:+0.013 / f2:+0.009 / f3:+0.015 / f4:-0.006 | 4 |
| supported − supported_random | overall | auroc | 5 | 0.004 | 0.014 | -0.014 | 0.021 | 3/5 | f0:-0.007 / f1:+0.002 / f2:+0.012 / f3:+0.023 / f4:-0.011 | 3 |
| supported − supported_random | overall | brier | 5 | -0.001 | 0.011 | -0.014 | 0.013 | 3/5 | f0:+0.014 / f1:-0.004 / f2:-0.010 / f3:-0.010 / f4:+0.006 | 3 |
| supported − supported_random | split_vote | acc | 5 | 0.010 | 0.014 | -0.008 | 0.028 | 3/5 | f0:-0.003 / f1:+0.021 / f2:+0.008 / f3:+0.028 / f4:-0.005 | 3 |
| supported − supported_conf | overall | acc | 5 | -0.006 | 0.011 | -0.020 | 0.008 | 1/5 | f0:-0.021 / f1:+0.010 / f2:-0.009 / f3:-0.004 / f4:-0.007 | 4 |
| supported − supported_conf | overall | bal_acc | 5 | -0.011 | 0.012 | -0.026 | 0.005 | 1/5 | f0:-0.015 / f1:+0.008 / f2:-0.009 / f3:-0.026 / f4:-0.011 | 4 |
| supported − supported_conf | overall | auroc | 5 | -0.004 | 0.004 | -0.009 | 0.001 | 1/5 | f0:-0.003 / f1:+0.002 / f2:-0.008 / f3:-0.008 / f4:-0.005 | 4 |
| supported − supported_conf | overall | brier | 5 | 0.003 | 0.007 | -0.006 | 0.012 | 2/5 | f0:+0.012 / f1:-0.003 / f2:+0.007 / f3:-0.005 / f4:+0.002 | 3 |
| supported − supported_conf | split_vote | acc | 5 | -0.010 | 0.016 | -0.030 | 0.010 | 2/5 | f0:-0.034 / f1:+0.006 / f2:-0.014 / f3:+0.003 / f4:-0.012 | 3 |
| joint − worstcase | overall | acc | 5 | -0.004 | 0.016 | -0.024 | 0.015 | 1/5 | f0:-0.020 / f1:+0.020 / f2:+0.000 / f3:-0.015 / f4:-0.006 | 3 |
| joint − worstcase | overall | bal_acc | 5 | -0.002 | 0.011 | -0.016 | 0.012 | 2/5 | f0:-0.017 / f1:+0.002 / f2:+0.013 / f3:-0.006 / f4:-0.003 | 3 |
| joint − worstcase | overall | auroc | 5 | -0.006 | 0.008 | -0.016 | 0.004 | 1/5 | f0:-0.003 / f1:+0.000 / f2:+0.000 / f3:-0.019 / f4:-0.006 | 3 |
| joint − worstcase | overall | brier | 5 | 0.006 | 0.011 | -0.007 | 0.019 | 1/5 | f0:+0.011 / f1:-0.010 / f2:+0.005 / f3:+0.019 / f4:+0.005 | 4 |
| joint − worstcase | split_vote | acc | 5 | -0.009 | 0.020 | -0.033 | 0.016 | 1/5 | f0:-0.027 / f1:+0.021 / f2:-0.003 / f3:-0.026 / f4:-0.008 | 4 |
| joint − interval | overall | acc | 5 | -0.007 | 0.014 | -0.025 | 0.010 | 2/5 | f0:-0.014 / f1:+0.005 / f2:-0.001 / f3:-0.029 / f4:+0.002 | 3 |
| joint − interval | overall | bal_acc | 5 | -0.007 | 0.013 | -0.023 | 0.009 | 3/5 | f0:-0.013 / f1:+0.002 / f2:+0.000 / f3:-0.027 / f4:+0.003 | 2 |
| joint − interval | overall | auroc | 5 | -0.007 | 0.009 | -0.018 | 0.003 | 1/5 | f0:-0.015 / f1:+0.003 / f2:-0.001 / f3:-0.018 / f4:-0.006 | 4 |
| joint − interval | overall | brier | 5 | 0.007 | 0.008 | -0.003 | 0.018 | 1/5 | f0:+0.013 / f1:-0.002 / f2:+0.003 / f3:+0.018 / f4:+0.004 | 4 |
| joint − interval | split_vote | acc | 5 | -0.009 | 0.020 | -0.034 | 0.017 | 2/5 | f0:-0.015 / f1:+0.006 / f2:+0.000 / f3:-0.041 / f4:+0.008 | 2 |
| supported − supervised_soft | overall | acc | 5 | 0.001 | 0.013 | -0.015 | 0.016 | 3/5 | f0:+0.009 / f1:+0.014 / f2:-0.018 / f3:-0.002 / f4:+0.001 | 3 |
| supported − supervised_soft | overall | bal_acc | 5 | 0.011 | 0.015 | -0.007 | 0.029 | 4/5 | f0:+0.021 / f1:+0.012 / f2:-0.013 / f3:+0.010 / f4:+0.025 | 4 |
| supported − supervised_soft | overall | auroc | 5 | 0.007 | 0.006 | -0.000 | 0.015 | 4/5 | f0:+0.010 / f1:+0.003 / f2:+0.000 / f3:+0.016 / f4:+0.008 | 4 |
| supported − supervised_soft | overall | brier | 5 | 0.005 | 0.009 | -0.006 | 0.015 | 2/5 | f0:+0.014 / f1:-0.004 / f2:+0.011 / f3:+0.007 / f4:-0.004 | 3 |
| supported − supervised_soft | split_vote | acc | 5 | -0.004 | 0.014 | -0.021 | 0.014 | 2/5 | f0:+0.009 / f1:+0.014 / f2:-0.014 / f3:-0.017 / f4:-0.011 | 3 |
| supported_random − supervised_soft | overall | acc | 5 | -0.008 | 0.017 | -0.030 | 0.013 | 2/5 | f0:+0.008 / f1:-0.003 / f2:-0.029 / f3:-0.025 / f4:+0.007 | 3 |
| supported_random − supervised_soft | overall | bal_acc | 5 | 0.005 | 0.021 | -0.021 | 0.030 | 2/5 | f0:+0.019 / f1:-0.001 / f2:-0.022 / f3:-0.005 / f4:+0.031 | 2 |
| supported_random − supervised_soft | overall | auroc | 5 | 0.004 | 0.014 | -0.014 | 0.021 | 3/5 | f0:+0.017 / f1:+0.001 / f2:-0.012 / f3:-0.007 / f4:+0.020 | 3 |
| supported_random − supervised_soft | overall | brier | 5 | 0.006 | 0.013 | -0.011 | 0.022 | 3/5 | f0:-0.000 / f1:-0.000 / f2:+0.021 / f3:+0.017 / f4:-0.010 | 2 |
| supported_random − supervised_soft | split_vote | acc | 5 | -0.013 | 0.021 | -0.039 | 0.013 | 1/5 | f0:+0.012 / f1:-0.008 / f2:-0.021 / f3:-0.044 / f4:-0.006 | 4 |
| supported_conf − supervised_soft | overall | acc | 5 | 0.007 | 0.015 | -0.011 | 0.025 | 4/5 | f0:+0.031 / f1:+0.004 / f2:-0.009 / f3:+0.002 / f4:+0.008 | 4 |
| supported_conf − supervised_soft | overall | bal_acc | 5 | 0.022 | 0.020 | -0.003 | 0.046 | 4/5 | f0:+0.035 / f1:+0.004 / f2:-0.004 / f3:+0.036 / f4:+0.036 | 4 |
| supported_conf − supervised_soft | overall | auroc | 5 | 0.012 | 0.008 | 0.001 | 0.022 | 5/5 | f0:+0.013 / f1:+0.001 / f2:+0.008 / f3:+0.024 / f4:+0.013 | 5 |
| supported_conf − supervised_soft | overall | brier | 5 | 0.002 | 0.007 | -0.006 | 0.011 | 2/5 | f0:+0.002 / f1:-0.001 / f2:+0.004 / f3:+0.012 / f4:-0.006 | 3 |
| supported_conf − supervised_soft | split_vote | acc | 5 | 0.006 | 0.023 | -0.022 | 0.035 | 3/5 | f0:+0.043 / f1:+0.008 / f2:+0.000 / f3:-0.020 / f4:+0.002 | 3 |
| interval − supervised_soft | overall | acc | 5 | 0.006 | 0.014 | -0.012 | 0.023 | 4/5 | f0:+0.012 / f1:+0.002 / f2:-0.017 / f3:+0.015 / f4:+0.015 | 4 |
| interval − supervised_soft | overall | bal_acc | 5 | 0.015 | 0.018 | -0.007 | 0.037 | 3/5 | f0:+0.021 / f1:-0.003 / f2:-0.005 / f3:+0.026 / f4:+0.035 | 3 |
| interval − supervised_soft | overall | auroc | 5 | 0.014 | 0.011 | 0.000 | 0.027 | 4/5 | f0:+0.016 / f1:-0.001 / f2:+0.006 / f3:+0.024 / f4:+0.022 | 4 |
| interval − supervised_soft | overall | brier | 5 | 0.001 | 0.008 | -0.008 | 0.011 | 1/5 | f0:+0.005 / f1:+0.003 / f2:+0.010 / f3:+0.001 / f4:-0.011 | 4 |
| interval − supervised_soft | split_vote | acc | 5 | 0.002 | 0.013 | -0.015 | 0.018 | 4/5 | f0:+0.012 / f1:+0.006 / f2:-0.021 / f3:+0.005 / f4:+0.006 | 4 |
| worstcase − supervised_soft | overall | acc | 5 | 0.002 | 0.019 | -0.021 | 0.026 | 3/5 | f0:+0.018 / f1:-0.013 / f2:-0.018 / f3:+0.002 / f4:+0.023 | 3 |
| worstcase − supervised_soft | overall | bal_acc | 5 | 0.010 | 0.023 | -0.018 | 0.039 | 3/5 | f0:+0.026 / f1:-0.004 / f2:-0.017 / f3:+0.005 / f4:+0.041 | 3 |
| worstcase − supervised_soft | overall | auroc | 5 | 0.012 | 0.011 | -0.002 | 0.026 | 5/5 | f0:+0.005 / f1:+0.001 / f2:+0.005 / f3:+0.026 / f4:+0.022 | 5 |
| worstcase − supervised_soft | overall | brier | 5 | 0.003 | 0.009 | -0.009 | 0.014 | 1/5 | f0:+0.007 / f1:+0.010 / f2:+0.008 / f3:+0.000 / f4:-0.012 | 4 |
| worstcase − supervised_soft | split_vote | acc | 5 | 0.002 | 0.020 | -0.023 | 0.026 | 2/5 | f0:+0.024 / f1:-0.009 / f2:-0.018 / f3:-0.011 / f4:+0.021 | 2 |
| joint − supervised_soft | overall | acc | 5 | -0.002 | 0.015 | -0.020 | 0.016 | 2/5 | f0:-0.002 / f1:+0.007 / f2:-0.018 / f3:-0.013 / f4:+0.017 | 3 |
| joint − supervised_soft | overall | bal_acc | 5 | 0.008 | 0.017 | -0.014 | 0.030 | 2/5 | f0:+0.008 / f1:-0.001 / f2:-0.004 / f3:-0.001 / f4:+0.038 | 2 |
| joint − supervised_soft | overall | auroc | 5 | 0.006 | 0.006 | -0.001 | 0.014 | 5/5 | f0:+0.002 / f1:+0.002 / f2:+0.005 / f3:+0.006 / f4:+0.016 | 5 |
| joint − supervised_soft | overall | brier | 5 | 0.009 | 0.012 | -0.006 | 0.023 | 1/5 | f0:+0.018 / f1:+0.001 / f2:+0.013 / f3:+0.019 / f4:-0.008 | 4 |
| joint − supervised_soft | split_vote | acc | 5 | -0.007 | 0.022 | -0.034 | 0.020 | 2/5 | f0:-0.003 / f1:+0.012 / f2:-0.021 / f3:-0.037 / f4:+0.014 | 3 |

## 3. Effect of Stage III (after − before, paired within run)

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | acc | 5 | 0.003 | 0.010 | -0.010 | 0.016 | 2/5 | f0:-0.001 / f1:+0.011 / f2:-0.009 / f3:-0.002 / f4:+0.016 | 2 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | bal_acc | 5 | 0.023 | 0.016 | 0.003 | 0.043 | 5/5 | f0:+0.003 / f1:+0.037 / f2:+0.016 / f3:+0.017 / f4:+0.041 | 5 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | auroc | 5 | 0.019 | 0.007 | 0.010 | 0.028 | 5/5 | f0:+0.013 / f1:+0.020 / f2:+0.012 / f3:+0.030 / f4:+0.020 | 5 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | unanimous | acc | 5 | 0.017 | 0.012 | 0.002 | 0.033 | 5/5 | f0:+0.015 / f1:+0.034 / f2:+0.009 / f3:+0.003 / f4:+0.025 | 5 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | split_vote | acc | 5 | -0.004 | 0.011 | -0.018 | 0.010 | 1/5 | f0:-0.009 / f1:+0.000 / f2:-0.018 / f3:-0.005 / f4:+0.012 | 3 |

### Every run: before (pre) / after (post) Stage III

| run | pre_acc | pre_bal_acc | pre_split_vote_acc | pre_unanimous_acc | post_acc | post_bal_acc | post_split_vote_acc | post_unanimous_acc |
|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl_soft | 0.780 | 0.789 | 0.714 | 0.913 | 0.779 | 0.792 | 0.705 | 0.929 |
| f1s1_hsrl_soft | 0.791 | 0.766 | 0.745 | 0.885 | 0.802 | 0.802 | 0.745 | 0.919 |
| f2s2_hsrl_soft | 0.766 | 0.742 | 0.726 | 0.845 | 0.756 | 0.757 | 0.708 | 0.855 |
| f3s3_hsrl_soft | 0.729 | 0.714 | 0.667 | 0.855 | 0.727 | 0.731 | 0.662 | 0.858 |
| f4s4_hsrl_soft | 0.770 | 0.733 | 0.731 | 0.848 | 0.786 | 0.774 | 0.743 | 0.873 |

## 4. Stage III pseudo-labels (vs hidden majority labels)

| config | runs | coverage | precision | prec_unanimous | prec_split | min_coverage |
|---|---|---|---|---|---|---|
| hsrl_soft | 5 | 0.299 ± 0.041 | 0.977 ± 0.006 | 0.996 ± 0.005 | 0.959 ± 0.010 | 0.266 |
| interval | 5 | 0.439 ± 0.034 | 0.962 ± 0.003 | 0.994 ± 0.002 | 0.932 ± 0.006 | 0.395 |
| joint | 5 | 0.441 ± 0.033 | 0.959 ± 0.009 | 0.994 ± 0.003 | 0.927 ± 0.017 | 0.399 |
| supported | 5 | 0.325 ± 0.018 | 0.976 ± 0.005 | 0.996 ± 0.005 | 0.955 ± 0.007 | 0.307 |
| supported_conf | 5 | 0.293 ± 0.030 | 0.976 ± 0.008 | 0.995 ± 0.005 | 0.957 ± 0.016 | 0.255 |
| supported_random | 5 | 0.285 ± 0.022 | 0.982 ± 0.008 | 0.995 ± 0.005 | 0.968 ± 0.014 | 0.252 |
| worstcase | 5 | 0.434 ± 0.031 | 0.961 ± 0.008 | 0.995 ± 0.003 | 0.931 ± 0.016 | 0.386 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl_soft | 5 | 30 | 1/5 | 1/5 | 29 | 0.146 ± 0.043 | 1.453 ± 0.388 | 0.764 ± 0.065 | 0.28/0.43/0.06 |
| interval | 5 | 30 | 0/5 | 0/5 | - | 1.579 ± 0.049 | 1.730 ± 0.034 | 0.785 ± 0.047 | 0.36/0.34/0.12 |
| joint | 5 | 30 | 0/5 | 0/5 | - | 1.605 ± 0.046 | 1.804 ± 0.051 | 0.779 ± 0.049 | 0.66/0.41/0.22 |
| supported | 5 | 30 | 0/5 | 0/5 | - | 0.264 ± 0.058 | 1.678 ± 0.082 | 0.769 ± 0.058 | 0.05/0.04/0.01 |
| supported_conf | 5 | 30 | 0/5 | 0/5 | - | 0.228 ± 0.057 | 1.647 ± 0.144 | 0.774 ± 0.045 | 0.06/0.08/0.01 |
| supported_random | 5 | 30 | 1/5 | 1/5 | 24 | 0.166 ± 0.043 | 1.660 ± 0.191 | 0.761 ± 0.046 | 0.12/0.09/0.02 |
| worstcase | 5 | 30 | 0/5 | 0/5 | - | 1.612 ± 0.049 | 1.789 ± 0.031 | 0.764 ± 0.056 | 0.70/0.43/0.24 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl_soft | 0.903 | 0.196 | 8 | nan | nan | 1.697 | 0.826 |
| f1s1_hsrl_soft | 0.882 | 0.170 | 11 | nan | nan | 1.773 | 0.832 |
| f2s2_hsrl_soft | 0.768 | 0.131 | 9 | nan | nan | 1.503 | 0.681 |
| f3s3_hsrl_soft | 0.946 | 0.081 | 19 | 13.000 | 29.000 | 0.792 | 0.724 |
| f4s4_hsrl_soft | 0.998 | 0.153 | 12 | nan | nan | 1.500 | 0.756 |
| f0s0_interval | 0.903 | 1.537 | 0 | nan | nan | 1.735 | 0.788 |
| f0s0_joint | 0.903 | 1.536 | 0 | nan | nan | 1.850 | 0.829 |
| f0s0_supported | 0.903 | 0.296 | 5 | nan | nan | 1.738 | 0.851 |
| f0s0_supported_conf | 0.903 | 0.268 | 6 | nan | nan | 1.837 | 0.806 |
| f0s0_supported_random | 0.903 | 0.198 | 7 | nan | nan | 1.814 | 0.802 |
| f0s0_worstcase | 0.903 | 1.546 | 0 | nan | nan | 1.754 | 0.772 |
| f1s1_interval | 0.882 | 1.588 | 28 | nan | nan | 1.716 | 0.852 |
| f1s1_joint | 0.882 | 1.631 | 0 | nan | nan | 1.826 | 0.829 |
| f1s1_supported | 0.882 | 0.277 | 6 | nan | nan | 1.769 | 0.800 |
| f1s1_supported_conf | 0.882 | 0.251 | 7 | nan | nan | 1.709 | 0.815 |
| f1s1_supported_random | 0.882 | 0.178 | 8 | nan | nan | 1.762 | 0.808 |
| f1s1_worstcase | 0.882 | 1.620 | 0 | nan | nan | 1.838 | 0.840 |
| f2s2_interval | 0.768 | 1.659 | 0 | nan | nan | 1.765 | 0.721 |
| f2s2_joint | 0.768 | 1.650 | 0 | nan | nan | 1.834 | 0.732 |
| f2s2_supported | 0.768 | 0.243 | 5 | nan | nan | 1.593 | 0.705 |
| f2s2_supported_conf | 0.768 | 0.208 | 6 | nan | nan | 1.523 | 0.734 |
| f2s2_supported_random | 0.768 | 0.170 | 8 | nan | nan | 1.819 | 0.719 |
| f2s2_worstcase | 0.768 | 1.653 | 0 | nan | nan | 1.777 | 0.683 |
| f3s3_interval | 0.946 | 1.567 | 18 | nan | nan | 1.752 | 0.793 |
| f3s3_joint | 0.946 | 1.628 | 20 | nan | nan | 1.791 | 0.774 |
| f3s3_supported | 0.946 | 0.176 | 10 | nan | nan | 1.697 | 0.734 |
| f3s3_supported_conf | 0.946 | 0.137 | 12 | nan | nan | 1.681 | 0.799 |
| f3s3_supported_random | 0.946 | 0.092 | 15 | 14.000 | 24.000 | 1.438 | 0.767 |
| f3s3_worstcase | 0.946 | 1.662 | 18 | nan | nan | 1.781 | 0.775 |
| f4s4_interval | 0.998 | 1.545 | 0 | nan | nan | 1.679 | 0.771 |
| f4s4_joint | 0.998 | 1.578 | 0 | nan | nan | 1.721 | 0.730 |
| f4s4_supported | 0.998 | 0.328 | 5 | nan | nan | 1.591 | 0.755 |
| f4s4_supported_conf | 0.998 | 0.275 | 6 | nan | nan | 1.486 | 0.718 |
| f4s4_supported_random | 0.998 | 0.193 | 10 | nan | nan | 1.467 | 0.710 |
| f4s4_worstcase | 0.998 | 1.579 | 0 | nan | nan | 1.797 | 0.750 |
