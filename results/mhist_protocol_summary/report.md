# Aggregate over results/mhist, results/mhist_protocol

Runs: 40; folds [0, 1, 2, 3, 4]; seeds [0, 1, 2, 3, 4]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl | 5 | 0.776 ± 0.022 | 0.752 ± 0.030 | 0.754 ± 0.025 | 0.855 ± 0.025 | 0.169 ± 0.017 | 0.871 ± 0.037 | 0.728 ± 0.031 |
| supervised | 5 | 0.767 ± 0.028 | 0.749 ± 0.028 | 0.749 ± 0.027 | 0.842 ± 0.033 | 0.187 ± 0.024 | 0.865 ± 0.032 | 0.719 ± 0.036 |
| hsrl_all10 | 5 | 0.801 ± 0.025 | 0.779 ± 0.024 | 0.783 ± 0.026 | 0.877 ± 0.021 | 0.152 ± 0.020 | 0.888 ± 0.019 | 0.758 ± 0.030 |
| hsrl_epochlog | 5 | 0.776 ± 0.022 | 0.752 ± 0.030 | 0.754 ± 0.025 | 0.855 ± 0.025 | 0.169 ± 0.017 | 0.871 ± 0.037 | 0.728 ± 0.031 |
| hsrl_r288 | 5 | 0.791 ± 0.031 | 0.771 ± 0.035 | 0.773 ± 0.034 | 0.865 ± 0.036 | 0.161 ± 0.028 | 0.884 ± 0.029 | 0.745 ± 0.035 |
| supervised_all10 | 5 | 0.791 ± 0.024 | 0.773 ± 0.039 | 0.772 ± 0.032 | 0.869 ± 0.023 | 0.166 ± 0.016 | 0.882 ± 0.031 | 0.746 ± 0.028 |
| supervised_epochlog | 5 | 0.767 ± 0.028 | 0.749 ± 0.028 | 0.749 ± 0.027 | 0.842 ± 0.033 | 0.187 ± 0.024 | 0.865 ± 0.032 | 0.719 ± 0.036 |
| supervised_r288 | 5 | 0.777 ± 0.037 | 0.754 ± 0.046 | 0.756 ± 0.043 | 0.838 ± 0.049 | 0.184 ± 0.036 | 0.864 ± 0.049 | 0.734 ± 0.036 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl | 0 | 1 | 0.784 | 0.790 | 0.875 | 0.713 |
| supervised | 0 | 1 | 0.787 | 0.782 | 0.873 | 0.728 |
| hsrl | 1 | 1 | 0.802 | 0.777 | 0.878 | 0.761 |
| supervised | 1 | 1 | 0.785 | 0.768 | 0.877 | 0.734 |
| hsrl | 2 | 1 | 0.773 | 0.743 | 0.848 | 0.734 |
| supervised | 2 | 1 | 0.766 | 0.751 | 0.818 | 0.723 |
| hsrl | 3 | 1 | 0.741 | 0.722 | 0.817 | 0.683 |
| supervised | 3 | 1 | 0.721 | 0.711 | 0.800 | 0.657 |
| hsrl | 4 | 1 | 0.778 | 0.730 | 0.857 | 0.751 |
| supervised | 4 | 1 | 0.779 | 0.732 | 0.842 | 0.754 |
| hsrl_all10 | 0 | 1 | 0.815 | 0.799 | 0.888 | 0.766 |
| hsrl_epochlog | 0 | 1 | 0.784 | 0.790 | 0.875 | 0.713 |
| hsrl_r288 | 0 | 1 | 0.788 | 0.783 | 0.875 | 0.729 |
| supervised_all10 | 0 | 1 | 0.790 | 0.797 | 0.880 | 0.729 |
| supervised_epochlog | 0 | 1 | 0.787 | 0.782 | 0.873 | 0.728 |
| supervised_r288 | 0 | 1 | 0.814 | 0.813 | 0.877 | 0.757 |
| hsrl_all10 | 1 | 1 | 0.831 | 0.801 | 0.902 | 0.797 |
| hsrl_epochlog | 1 | 1 | 0.802 | 0.777 | 0.878 | 0.761 |
| hsrl_r288 | 1 | 1 | 0.822 | 0.799 | 0.889 | 0.784 |
| supervised_all10 | 1 | 1 | 0.817 | 0.804 | 0.887 | 0.781 |
| supervised_epochlog | 1 | 1 | 0.785 | 0.768 | 0.877 | 0.734 |
| supervised_r288 | 1 | 1 | 0.808 | 0.776 | 0.876 | 0.769 |
| hsrl_all10 | 2 | 1 | 0.785 | 0.778 | 0.867 | 0.737 |
| hsrl_epochlog | 2 | 1 | 0.773 | 0.743 | 0.848 | 0.734 |
| hsrl_r288 | 2 | 1 | 0.800 | 0.787 | 0.873 | 0.754 |
| supervised_all10 | 2 | 1 | 0.804 | 0.802 | 0.884 | 0.752 |
| supervised_epochlog | 2 | 1 | 0.766 | 0.751 | 0.818 | 0.723 |
| supervised_r288 | 2 | 1 | 0.757 | 0.747 | 0.817 | 0.703 |
| hsrl_all10 | 3 | 1 | 0.768 | 0.741 | 0.847 | 0.720 |
| hsrl_epochlog | 3 | 1 | 0.741 | 0.722 | 0.817 | 0.683 |
| hsrl_r288 | 3 | 1 | 0.740 | 0.710 | 0.802 | 0.694 |
| supervised_all10 | 3 | 1 | 0.753 | 0.719 | 0.832 | 0.708 |
| supervised_epochlog | 3 | 1 | 0.721 | 0.711 | 0.800 | 0.657 |
| supervised_r288 | 3 | 1 | 0.725 | 0.688 | 0.762 | 0.688 |
| hsrl_all10 | 4 | 1 | 0.808 | 0.778 | 0.882 | 0.772 |
| hsrl_epochlog | 4 | 1 | 0.778 | 0.730 | 0.857 | 0.751 |
| hsrl_r288 | 4 | 1 | 0.804 | 0.773 | 0.887 | 0.764 |
| supervised_all10 | 4 | 1 | 0.789 | 0.743 | 0.863 | 0.757 |
| supervised_epochlog | 4 | 1 | 0.779 | 0.732 | 0.842 | 0.754 |
| supervised_r288 | 4 | 1 | 0.780 | 0.747 | 0.859 | 0.751 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| supervised_all10 − supervised | overall | acc | 5 | 0.023 | 0.016 | 0.004 | 0.043 | 5/5 | f0:+0.003 / f1:+0.032 / f2:+0.039 / f3:+0.033 / f4:+0.010 | 5 |
| supervised_all10 − supervised | overall | bal_acc | 5 | 0.025 | 0.018 | 0.002 | 0.048 | 5/5 | f0:+0.016 / f1:+0.036 / f2:+0.052 / f3:+0.009 / f4:+0.012 | 5 |
| supervised_all10 − supervised | overall | auroc | 5 | 0.027 | 0.024 | -0.002 | 0.056 | 5/5 | f0:+0.007 / f1:+0.010 / f2:+0.066 / f3:+0.031 / f4:+0.021 | 5 |
| supervised_all10 − supervised | overall | brier | 5 | -0.021 | 0.018 | -0.044 | 0.001 | 4/5 | f0:+0.001 / f1:-0.018 / f2:-0.045 / f3:-0.033 / f4:-0.010 | 4 |
| supervised_all10 − supervised | split_vote | acc | 5 | 0.026 | 0.023 | -0.003 | 0.055 | 5/5 | f0:+0.002 / f1:+0.047 / f2:+0.029 / f3:+0.050 / f4:+0.003 | 5 |
| hsrl_all10 − hsrl | overall | acc | 5 | 0.026 | 0.008 | 0.016 | 0.035 | 5/5 | f0:+0.031 / f1:+0.029 / f2:+0.012 / f3:+0.027 / f4:+0.030 | 5 |
| hsrl_all10 − hsrl | overall | bal_acc | 5 | 0.027 | 0.015 | 0.008 | 0.045 | 5/5 | f0:+0.009 / f1:+0.024 / f2:+0.035 / f3:+0.019 / f4:+0.047 | 5 |
| hsrl_all10 − hsrl | overall | auroc | 5 | 0.022 | 0.007 | 0.014 | 0.030 | 5/5 | f0:+0.012 / f1:+0.024 / f2:+0.020 / f3:+0.030 / f4:+0.025 | 5 |
| hsrl_all10 − hsrl | overall | brier | 5 | -0.017 | 0.005 | -0.023 | -0.010 | 5/5 | f0:-0.018 / f1:-0.017 / f2:-0.011 / f3:-0.013 / f4:-0.024 | 5 |
| hsrl_all10 − hsrl | split_vote | acc | 5 | 0.030 | 0.019 | 0.007 | 0.053 | 5/5 | f0:+0.054 / f1:+0.035 / f2:+0.003 / f3:+0.037 / f4:+0.021 | 5 |
| supervised_r288 − supervised | overall | acc | 5 | 0.009 | 0.015 | -0.009 | 0.028 | 4/5 | f0:+0.027 / f1:+0.022 / f2:-0.008 / f3:+0.004 / f4:+0.001 | 4 |
| supervised_r288 − supervised | overall | bal_acc | 5 | 0.006 | 0.020 | -0.020 | 0.031 | 3/5 | f0:+0.032 / f1:+0.009 / f2:-0.004 / f3:-0.023 / f4:+0.015 | 3 |
| supervised_r288 − supervised | overall | auroc | 5 | -0.004 | 0.021 | -0.030 | 0.022 | 2/5 | f0:+0.004 / f1:-0.001 / f2:-0.002 / f3:-0.039 / f4:+0.017 | 3 |
| supervised_r288 − supervised | overall | brier | 5 | -0.003 | 0.013 | -0.019 | 0.014 | 3/5 | f0:-0.018 / f1:-0.009 / f2:+0.000 / f3:+0.018 / f4:-0.006 | 3 |
| supervised_r288 − supervised | split_vote | acc | 5 | 0.014 | 0.024 | -0.016 | 0.045 | 3/5 | f0:+0.029 / f1:+0.035 / f2:-0.020 / f3:+0.031 / f4:-0.003 | 3 |
| hsrl_r288 − hsrl | overall | acc | 5 | 0.015 | 0.013 | -0.001 | 0.032 | 4/5 | f0:+0.004 / f1:+0.019 / f2:+0.028 / f3:-0.001 / f4:+0.027 | 4 |
| hsrl_r288 − hsrl | overall | bal_acc | 5 | 0.018 | 0.027 | -0.015 | 0.051 | 3/5 | f0:-0.007 / f1:+0.022 / f2:+0.044 / f3:-0.012 / f4:+0.043 | 3 |
| hsrl_r288 − hsrl | overall | auroc | 5 | 0.010 | 0.018 | -0.013 | 0.033 | 4/5 | f0:+0.000 / f1:+0.011 / f2:+0.025 / f3:-0.015 / f4:+0.030 | 4 |
| hsrl_r288 − hsrl | overall | brier | 5 | -0.008 | 0.016 | -0.028 | 0.012 | 3/5 | f0:+0.001 / f1:-0.013 / f2:-0.020 / f3:+0.015 / f4:-0.023 | 3 |
| hsrl_r288 − hsrl | split_vote | acc | 5 | 0.017 | 0.005 | 0.011 | 0.023 | 5/5 | f0:+0.017 / f1:+0.023 / f2:+0.020 / f3:+0.011 / f4:+0.014 | 5 |
| hsrl_all10 − supervised_all10 | overall | acc | 5 | 0.010 | 0.017 | -0.011 | 0.032 | 4/5 | f0:+0.024 / f1:+0.014 / f2:-0.019 / f3:+0.014 / f4:+0.018 | 4 |
| hsrl_all10 − supervised_all10 | overall | bal_acc | 5 | 0.006 | 0.023 | -0.022 | 0.034 | 3/5 | f0:+0.002 / f1:-0.003 / f2:-0.025 / f3:+0.022 / f4:+0.034 | 3 |
| hsrl_all10 − supervised_all10 | overall | auroc | 5 | 0.008 | 0.014 | -0.010 | 0.026 | 4/5 | f0:+0.008 / f1:+0.015 / f2:-0.017 / f3:+0.015 / f4:+0.020 | 4 |
| hsrl_all10 − supervised_all10 | overall | brier | 5 | -0.014 | 0.016 | -0.034 | 0.006 | 4/5 | f0:-0.028 / f1:-0.014 / f2:+0.010 / f3:-0.008 / f4:-0.029 | 4 |
| hsrl_all10 − supervised_all10 | split_vote | acc | 5 | 0.013 | 0.019 | -0.010 | 0.036 | 4/5 | f0:+0.037 / f1:+0.015 / f2:-0.015 / f3:+0.012 / f4:+0.015 | 4 |
| hsrl_r288 − supervised_r288 | overall | acc | 5 | 0.014 | 0.025 | -0.017 | 0.046 | 4/5 | f0:-0.026 / f1:+0.014 / f2:+0.043 / f3:+0.015 / f4:+0.025 | 4 |
| hsrl_r288 − supervised_r288 | overall | bal_acc | 5 | 0.016 | 0.027 | -0.017 | 0.050 | 4/5 | f0:-0.030 / f1:+0.022 / f2:+0.040 / f3:+0.023 / f4:+0.027 | 4 |
| hsrl_r288 − supervised_r288 | overall | auroc | 5 | 0.027 | 0.023 | -0.001 | 0.055 | 4/5 | f0:-0.002 / f1:+0.013 / f2:+0.056 / f3:+0.040 / f4:+0.029 | 4 |
| hsrl_r288 − supervised_r288 | overall | brier | 5 | -0.023 | 0.020 | -0.049 | 0.002 | 4/5 | f0:+0.010 / f1:-0.019 / f2:-0.044 / f3:-0.031 / f4:-0.032 | 4 |
| hsrl_r288 − supervised_r288 | split_vote | acc | 5 | 0.012 | 0.028 | -0.023 | 0.046 | 4/5 | f0:-0.027 / f1:+0.015 / f2:+0.050 / f3:+0.006 / f4:+0.014 | 4 |

## 3. Effect of Stage III (after − before, paired within run)

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl[final] − hsrl[before_stage3] | overall | acc | 5 | 0.010 | 0.008 | 0.000 | 0.020 | 4/5 | f0:+0.020 / f1:+0.012 / f2:+0.013 / f3:+0.004 / f4:+0.000 | 4 |
| hsrl[final] − hsrl[before_stage3] | overall | bal_acc | 5 | 0.005 | 0.011 | -0.009 | 0.019 | 4/5 | f0:+0.021 / f1:+0.006 / f2:+0.008 / f3:+0.002 / f4:-0.010 | 4 |
| hsrl[final] − hsrl[before_stage3] | overall | auroc | 5 | 0.012 | 0.007 | 0.004 | 0.020 | 5/5 | f0:+0.021 / f1:+0.011 / f2:+0.008 / f3:+0.015 / f4:+0.004 | 5 |
| hsrl[final] − hsrl[before_stage3] | unanimous | acc | 5 | 0.007 | 0.011 | -0.007 | 0.021 | 3/5 | f0:+0.022 / f1:+0.003 / f2:+0.016 / f3:+0.000 / f4:-0.006 | 3 |
| hsrl[final] − hsrl[before_stage3] | split_vote | acc | 5 | 0.012 | 0.007 | 0.003 | 0.020 | 5/5 | f0:+0.020 / f1:+0.017 / f2:+0.012 / f3:+0.006 / f4:+0.003 | 5 |
| hsrl_all10[final] − hsrl_all10[before_stage3] | overall | acc | 5 | 0.014 | 0.009 | 0.003 | 0.025 | 5/5 | f0:+0.016 / f1:+0.015 / f2:+0.002 / f3:+0.027 / f4:+0.011 | 5 |
| hsrl_all10[final] − hsrl_all10[before_stage3] | overall | bal_acc | 5 | 0.008 | 0.008 | -0.002 | 0.018 | 4/5 | f0:+0.009 / f1:+0.012 / f2:+0.001 / f3:+0.019 / f4:-0.000 | 4 |
| hsrl_all10[final] − hsrl_all10[before_stage3] | overall | auroc | 5 | 0.010 | 0.006 | 0.003 | 0.018 | 5/5 | f0:+0.012 / f1:+0.006 / f2:+0.004 / f3:+0.019 / f4:+0.012 | 5 |
| hsrl_all10[final] − hsrl_all10[before_stage3] | unanimous | acc | 5 | 0.015 | 0.007 | 0.006 | 0.024 | 5/5 | f0:+0.019 / f1:+0.016 / f2:+0.009 / f3:+0.025 / f4:+0.006 | 5 |
| hsrl_all10[final] − hsrl_all10[before_stage3] | split_vote | acc | 5 | 0.014 | 0.010 | 0.001 | 0.027 | 4/5 | f0:+0.015 / f1:+0.015 / f2:-0.002 / f3:+0.027 / f4:+0.014 | 4 |
| hsrl_epochlog[final] − hsrl_epochlog[before_stage3] | overall | acc | 5 | 0.010 | 0.008 | 0.000 | 0.020 | 4/5 | f0:+0.020 / f1:+0.012 / f2:+0.013 / f3:+0.004 / f4:+0.000 | 4 |
| hsrl_epochlog[final] − hsrl_epochlog[before_stage3] | overall | bal_acc | 5 | 0.005 | 0.011 | -0.009 | 0.019 | 4/5 | f0:+0.021 / f1:+0.006 / f2:+0.008 / f3:+0.002 / f4:-0.010 | 4 |
| hsrl_epochlog[final] − hsrl_epochlog[before_stage3] | overall | auroc | 5 | 0.012 | 0.007 | 0.004 | 0.020 | 5/5 | f0:+0.021 / f1:+0.011 / f2:+0.008 / f3:+0.015 / f4:+0.004 | 5 |
| hsrl_epochlog[final] − hsrl_epochlog[before_stage3] | unanimous | acc | 5 | 0.007 | 0.011 | -0.007 | 0.021 | 3/5 | f0:+0.022 / f1:+0.003 / f2:+0.016 / f3:+0.000 / f4:-0.006 | 3 |
| hsrl_epochlog[final] − hsrl_epochlog[before_stage3] | split_vote | acc | 5 | 0.012 | 0.007 | 0.003 | 0.020 | 5/5 | f0:+0.020 / f1:+0.017 / f2:+0.012 / f3:+0.006 / f4:+0.003 | 5 |
| hsrl_r288[final] − hsrl_r288[before_stage3] | overall | acc | 5 | 0.013 | 0.007 | 0.004 | 0.022 | 5/5 | f0:+0.008 / f1:+0.016 / f2:+0.013 / f3:+0.004 / f4:+0.023 | 5 |
| hsrl_r288[final] − hsrl_r288[before_stage3] | overall | bal_acc | 5 | 0.011 | 0.008 | 0.001 | 0.022 | 5/5 | f0:+0.008 / f1:+0.012 / f2:+0.013 / f3:+0.000 / f4:+0.023 | 5 |
| hsrl_r288[final] − hsrl_r288[before_stage3] | overall | auroc | 5 | 0.009 | 0.006 | 0.001 | 0.017 | 5/5 | f0:+0.012 / f1:+0.004 / f2:+0.009 / f3:+0.002 / f4:+0.017 | 5 |
| hsrl_r288[final] − hsrl_r288[before_stage3] | unanimous | acc | 5 | 0.019 | 0.009 | 0.009 | 0.030 | 5/5 | f0:+0.022 / f1:+0.009 / f2:+0.022 / f3:+0.012 / f4:+0.031 | 5 |
| hsrl_r288[final] − hsrl_r288[before_stage3] | split_vote | acc | 5 | 0.010 | 0.010 | -0.002 | 0.022 | 4/5 | f0:+0.002 / f1:+0.020 / f2:+0.009 / f3:+0.000 / f4:+0.020 | 4 |

### Every run: before (pre) / after (post) Stage III

| run | pre_acc | pre_bal_acc | pre_split_vote_acc | pre_unanimous_acc | post_acc | post_bal_acc | post_split_vote_acc | post_unanimous_acc |
|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.764 | 0.769 | 0.693 | 0.907 | 0.784 | 0.790 | 0.713 | 0.929 |
| f0s0_hsrl_all10 | 0.798 | 0.790 | 0.751 | 0.895 | 0.815 | 0.799 | 0.766 | 0.913 |
| f0s0_hsrl_epochlog | 0.764 | 0.769 | 0.693 | 0.907 | 0.784 | 0.790 | 0.713 | 0.929 |
| f0s0_hsrl_r288 | 0.780 | 0.775 | 0.728 | 0.885 | 0.788 | 0.783 | 0.729 | 0.907 |
| f1s1_hsrl | 0.790 | 0.771 | 0.745 | 0.882 | 0.802 | 0.777 | 0.761 | 0.885 |
| f1s1_hsrl_all10 | 0.816 | 0.789 | 0.781 | 0.885 | 0.831 | 0.801 | 0.797 | 0.901 |
| f1s1_hsrl_epochlog | 0.790 | 0.771 | 0.745 | 0.882 | 0.802 | 0.777 | 0.761 | 0.885 |
| f1s1_hsrl_r288 | 0.805 | 0.787 | 0.764 | 0.888 | 0.822 | 0.799 | 0.784 | 0.898 |
| f2s2_hsrl | 0.759 | 0.734 | 0.722 | 0.836 | 0.773 | 0.743 | 0.734 | 0.851 |
| f2s2_hsrl_all10 | 0.783 | 0.777 | 0.739 | 0.873 | 0.785 | 0.778 | 0.737 | 0.882 |
| f2s2_hsrl_epochlog | 0.759 | 0.734 | 0.722 | 0.836 | 0.773 | 0.743 | 0.734 | 0.851 |
| f2s2_hsrl_r288 | 0.787 | 0.774 | 0.745 | 0.873 | 0.800 | 0.787 | 0.754 | 0.895 |
| f3s3_hsrl | 0.737 | 0.720 | 0.677 | 0.858 | 0.741 | 0.722 | 0.683 | 0.858 |
| f3s3_hsrl_all10 | 0.741 | 0.722 | 0.693 | 0.839 | 0.768 | 0.741 | 0.720 | 0.864 |
| f3s3_hsrl_epochlog | 0.737 | 0.720 | 0.677 | 0.858 | 0.741 | 0.722 | 0.683 | 0.858 |
| f3s3_hsrl_r288 | 0.736 | 0.710 | 0.694 | 0.820 | 0.740 | 0.710 | 0.694 | 0.833 |
| f4s4_hsrl | 0.778 | 0.741 | 0.748 | 0.839 | 0.778 | 0.730 | 0.751 | 0.833 |
| f4s4_hsrl_all10 | 0.796 | 0.778 | 0.758 | 0.873 | 0.808 | 0.778 | 0.772 | 0.879 |
| f4s4_hsrl_epochlog | 0.778 | 0.741 | 0.748 | 0.839 | 0.778 | 0.730 | 0.751 | 0.833 |
| f4s4_hsrl_r288 | 0.781 | 0.750 | 0.745 | 0.855 | 0.804 | 0.773 | 0.764 | 0.885 |

## 4. Stage III pseudo-labels (vs hidden majority labels)

| config | runs | coverage | precision | prec_unanimous | prec_split | min_coverage |
|---|---|---|---|---|---|---|
| hsrl | 5 | 0.703 ± 0.022 | 0.911 ± 0.006 | 0.978 ± 0.009 | 0.867 ± 0.010 | 0.678 |
| hsrl_all10 | 5 | 0.754 ± 0.039 | 0.913 ± 0.014 | 0.984 ± 0.005 | 0.868 ± 0.022 | 0.689 |
| hsrl_epochlog | 5 | 0.703 ± 0.022 | 0.911 ± 0.006 | 0.978 ± 0.009 | 0.867 ± 0.010 | 0.678 |
| hsrl_r288 | 5 | 0.703 ± 0.014 | 0.917 ± 0.015 | 0.979 ± 0.007 | 0.876 ± 0.023 | 0.684 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl | 5 | 30 | 1/5 | 1/5 | 29 | 0.146 ± 0.043 | 1.453 ± 0.388 | 0.764 ± 0.065 | 0.28/0.43/0.06 |
| hsrl_all10 | 5 | 30 | 2/5 | 2/5 | 20 22 | 0.107 ± 0.046 | 1.594 ± 0.081 | 0.787 ± 0.028 | 0.19/0.32/0.03 |
| hsrl_epochlog | 5 | 30 | 1/5 | 1/5 | 29 | 0.146 ± 0.043 | 1.453 ± 0.388 | 0.764 ± 0.065 | 0.28/0.43/0.06 |
| hsrl_r288 | 5 | 30 | 0/5 | 0/5 | - | 0.138 ± 0.044 | 1.567 ± 0.127 | 0.776 ± 0.039 | 0.14/0.34/0.02 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.903 | 0.196 | 8 | nan | nan | 1.697 | 0.826 |
| f1s1_hsrl | 0.882 | 0.170 | 11 | nan | nan | 1.773 | 0.832 |
| f2s2_hsrl | 0.768 | 0.131 | 9 | nan | nan | 1.503 | 0.681 |
| f3s3_hsrl | 0.946 | 0.081 | 19 | 13.000 | 29.000 | 0.792 | 0.724 |
| f4s4_hsrl | 0.998 | 0.153 | 12 | nan | nan | 1.500 | 0.756 |
| f0s0_hsrl_all10 | 0.903 | 0.181 | 7 | nan | nan | 1.635 | 0.801 |
| f0s0_hsrl_epochlog | 0.903 | 0.196 | 8 | nan | nan | 1.697 | 0.826 |
| f0s0_hsrl_r288 | 0.829 | 0.165 | 9 | nan | nan | 1.764 | 0.781 |
| f1s1_hsrl_all10 | 0.882 | 0.122 | 9 | nan | nan | 1.706 | 0.818 |
| f1s1_hsrl_epochlog | 0.882 | 0.170 | 11 | nan | nan | 1.773 | 0.832 |
| f1s1_hsrl_r288 | 0.784 | 0.198 | 7 | nan | nan | 1.549 | 0.827 |
| f2s2_hsrl_all10 | 0.768 | 0.080 | 14 | nan | nan | 1.585 | 0.762 |
| f2s2_hsrl_epochlog | 0.768 | 0.131 | 9 | nan | nan | 1.503 | 0.681 |
| f2s2_hsrl_r288 | 0.691 | 0.118 | 9 | nan | nan | 1.603 | 0.718 |
| f3s3_hsrl_all10 | 0.946 | 0.083 | 13 | 10.000 | 20.000 | 1.544 | 0.802 |
| f3s3_hsrl_epochlog | 0.946 | 0.081 | 19 | 13.000 | 29.000 | 0.792 | 0.724 |
| f3s3_hsrl_r288 | 0.858 | 0.087 | 13 | nan | nan | 1.441 | 0.777 |
| f4s4_hsrl_all10 | 0.998 | 0.070 | 15 | 8.000 | 22.000 | 1.498 | 0.754 |
| f4s4_hsrl_epochlog | 0.998 | 0.153 | 12 | nan | nan | 1.500 | 0.756 |
| f4s4_hsrl_r288 | 0.924 | 0.124 | 9 | nan | nan | 1.480 | 0.776 |
