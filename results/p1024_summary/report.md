# Aggregate over results/p1024

Runs: 60; folds [0, 1, 2]; seeds [0, 1, 2, 3, 4]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl | 15 | 0.824 ± 0.015 | 0.810 ± 0.020 | 0.811 ± 0.017 | 0.897 ± 0.008 | 0.133 ± 0.008 | 0.884 ± 0.015 | 0.672 ± 0.033 |
| hsrl_no_stage1 | 15 | 0.663 ± 0.033 | 0.696 ± 0.026 | 0.661 ± 0.032 | 0.780 ± 0.040 | 0.218 ± 0.010 | 0.665 ± 0.049 | 0.657 ± 0.031 |
| hsrl_no_t2 | 15 | 0.821 ± 0.016 | 0.806 ± 0.026 | 0.807 ± 0.022 | 0.895 ± 0.012 | 0.136 ± 0.011 | 0.883 ± 0.013 | 0.666 ± 0.037 |
| supervised | 15 | 0.824 ± 0.010 | 0.811 ± 0.013 | 0.811 ± 0.010 | 0.894 ± 0.008 | 0.140 ± 0.007 | 0.882 ± 0.014 | 0.676 ± 0.022 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl | 0 | 5 | 0.829 ± 0.017 | 0.805 ± 0.023 | 0.895 ± 0.011 | 0.682 ± 0.037 |
| hsrl_no_stage1 | 0 | 5 | 0.671 ± 0.029 | 0.708 ± 0.019 | 0.805 ± 0.024 | 0.669 ± 0.017 |
| hsrl_no_t2 | 0 | 5 | 0.818 ± 0.020 | 0.790 ± 0.035 | 0.891 ± 0.018 | 0.662 ± 0.053 |
| supervised | 0 | 5 | 0.830 ± 0.007 | 0.803 ± 0.011 | 0.893 ± 0.006 | 0.678 ± 0.032 |
| hsrl | 1 | 5 | 0.834 ± 0.005 | 0.826 ± 0.004 | 0.902 ± 0.003 | 0.685 ± 0.015 |
| hsrl_no_stage1 | 1 | 5 | 0.661 ± 0.051 | 0.677 ± 0.034 | 0.742 ± 0.045 | 0.628 ± 0.034 |
| hsrl_no_t2 | 1 | 5 | 0.832 ± 0.013 | 0.822 ± 0.013 | 0.896 ± 0.010 | 0.670 ± 0.031 |
| supervised | 1 | 5 | 0.823 ± 0.013 | 0.818 ± 0.016 | 0.887 ± 0.007 | 0.677 ± 0.017 |
| hsrl | 2 | 5 | 0.809 ± 0.010 | 0.799 ± 0.018 | 0.895 ± 0.006 | 0.650 ± 0.036 |
| hsrl_no_stage1 | 2 | 5 | 0.657 ± 0.017 | 0.702 ± 0.012 | 0.793 ± 0.010 | 0.675 ± 0.018 |
| hsrl_no_t2 | 2 | 5 | 0.815 ± 0.014 | 0.806 ± 0.020 | 0.897 ± 0.007 | 0.665 ± 0.029 |
| supervised | 2 | 5 | 0.818 ± 0.008 | 0.813 ± 0.009 | 0.900 ± 0.003 | 0.673 ± 0.019 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl − supervised | overall | acc | 15 | 0.000 | 0.016 | -0.009 | 0.009 | 7/15 | f0:-0.002 / f1:+0.011 / f2:-0.009 | 1 |
| hsrl − supervised | overall | bal_acc | 15 | -0.001 | 0.021 | -0.012 | 0.010 | 7/15 | f0:+0.002 / f1:+0.009 / f2:-0.014 | 1 |
| hsrl − supervised | overall | auroc | 15 | 0.004 | 0.012 | -0.003 | 0.010 | 9/15 | f0:+0.002 / f1:+0.015 / f2:-0.005 | 2 |
| hsrl − supervised | overall | brier | 15 | -0.007 | 0.010 | -0.012 | -0.001 | 10/15 | f0:-0.004 / f1:-0.014 / f2:-0.001 | 3 |
| hsrl − supervised | split_vote | acc | 15 | -0.004 | 0.032 | -0.021 | 0.014 | 8/15 | f0:+0.004 / f1:+0.008 / f2:-0.024 | 1 |
| hsrl − hsrl_no_t2 | overall | acc | 15 | 0.002 | 0.021 | -0.009 | 0.014 | 7/15 | f0:+0.011 / f1:+0.002 / f2:-0.006 | 2 |
| hsrl − hsrl_no_t2 | overall | bal_acc | 15 | 0.004 | 0.031 | -0.013 | 0.022 | 9/15 | f0:+0.015 / f1:+0.004 / f2:-0.007 | 2 |
| hsrl − hsrl_no_t2 | overall | auroc | 15 | 0.003 | 0.015 | -0.005 | 0.011 | 7/15 | f0:+0.004 / f1:+0.007 / f2:-0.002 | 2 |
| hsrl − hsrl_no_t2 | overall | brier | 15 | -0.002 | 0.013 | -0.009 | 0.005 | 7/15 | f0:-0.004 / f1:-0.004 / f2:+0.001 | 2 |
| hsrl − hsrl_no_t2 | split_vote | acc | 15 | 0.006 | 0.053 | -0.023 | 0.036 | 7/15 | f0:+0.020 / f1:+0.015 / f2:-0.015 | 2 |
| hsrl − hsrl_no_stage1 | overall | acc | 15 | 0.161 | 0.035 | 0.142 | 0.180 | 15/15 | f0:+0.158 / f1:+0.172 / f2:+0.152 | 3 |
| hsrl − hsrl_no_stage1 | overall | bal_acc | 15 | 0.115 | 0.034 | 0.096 | 0.134 | 15/15 | f0:+0.097 / f1:+0.149 / f2:+0.098 | 3 |
| hsrl − hsrl_no_stage1 | overall | auroc | 15 | 0.117 | 0.041 | 0.095 | 0.140 | 15/15 | f0:+0.090 / f1:+0.161 / f2:+0.102 | 3 |
| hsrl − hsrl_no_stage1 | overall | brier | 15 | -0.085 | 0.013 | -0.092 | -0.078 | 15/15 | f0:-0.083 / f1:-0.095 / f2:-0.078 | 3 |
| hsrl − hsrl_no_stage1 | split_vote | acc | 15 | 0.015 | 0.051 | -0.014 | 0.043 | 10/15 | f0:+0.013 / f1:+0.057 / f2:-0.025 | 2 |
| hsrl_no_t2 − supervised | overall | acc | 15 | -0.002 | 0.021 | -0.014 | 0.010 | 6/15 | f0:-0.013 / f1:+0.009 / f2:-0.003 | 2 |
| hsrl_no_t2 − supervised | overall | bal_acc | 15 | -0.005 | 0.027 | -0.020 | 0.010 | 7/15 | f0:-0.013 / f1:+0.004 / f2:-0.007 | 2 |
| hsrl_no_t2 − supervised | overall | auroc | 15 | 0.001 | 0.016 | -0.008 | 0.010 | 7/15 | f0:-0.002 / f1:+0.008 / f2:-0.003 | 1 |
| hsrl_no_t2 − supervised | overall | brier | 15 | -0.004 | 0.015 | -0.013 | 0.004 | 11/15 | f0:-0.000 / f1:-0.011 / f2:-0.002 | 3 |
| hsrl_no_t2 − supervised | split_vote | acc | 15 | -0.010 | 0.043 | -0.034 | 0.014 | 5/15 | f0:-0.016 / f1:-0.007 / f2:-0.008 | 3 |

## 3. Effect of Stage III (after − before, paired within run)

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl[final] − hsrl[before_stage3] | overall | acc | 15 | 0.017 | 0.010 | 0.012 | 0.023 | 14/15 | f0:+0.023 / f1:+0.018 / f2:+0.012 | 3 |
| hsrl[final] − hsrl[before_stage3] | overall | bal_acc | 15 | 0.019 | 0.011 | 0.013 | 0.025 | 15/15 | f0:+0.027 / f1:+0.016 / f2:+0.014 | 3 |
| hsrl[final] − hsrl[before_stage3] | overall | auroc | 15 | 0.013 | 0.006 | 0.010 | 0.017 | 15/15 | f0:+0.009 / f1:+0.016 / f2:+0.014 | 3 |
| hsrl[final] − hsrl[before_stage3] | unanimous | acc | 15 | 0.015 | 0.009 | 0.010 | 0.020 | 13/15 | f0:+0.015 / f1:+0.016 / f2:+0.014 | 3 |
| hsrl[final] − hsrl[before_stage3] | split_vote | acc | 15 | 0.023 | 0.022 | 0.010 | 0.035 | 13/15 | f0:+0.040 / f1:+0.022 / f2:+0.006 | 3 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | acc | 15 | -0.078 | 0.035 | -0.097 | -0.058 | 0/15 | f0:-0.089 / f1:-0.091 / f2:-0.054 | 3 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | bal_acc | 15 | -0.004 | 0.046 | -0.029 | 0.021 | 7/15 | f0:+0.001 / f1:-0.050 / f2:+0.038 | 1 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | auroc | 15 | -0.055 | 0.045 | -0.080 | -0.030 | 1/15 | f0:-0.053 / f1:-0.097 / f2:-0.015 | 3 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | unanimous | acc | 15 | -0.158 | 0.047 | -0.184 | -0.132 | 0/15 | f0:-0.176 / f1:-0.135 / f2:-0.163 | 3 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | split_vote | acc | 15 | 0.125 | 0.092 | 0.073 | 0.176 | 14/15 | f0:+0.110 / f1:+0.029 / f2:+0.234 | 3 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | overall | acc | 15 | 0.013 | 0.008 | 0.008 | 0.018 | 15/15 | f0:+0.015 / f1:+0.016 / f2:+0.009 | 3 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | overall | bal_acc | 15 | 0.017 | 0.011 | 0.011 | 0.023 | 14/15 | f0:+0.022 / f1:+0.019 / f2:+0.010 | 3 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | overall | auroc | 15 | 0.012 | 0.007 | 0.008 | 0.015 | 14/15 | f0:+0.008 / f1:+0.016 / f2:+0.011 | 3 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | unanimous | acc | 15 | 0.011 | 0.011 | 0.005 | 0.017 | 13/15 | f0:+0.007 / f1:+0.014 / f2:+0.011 | 3 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | split_vote | acc | 15 | 0.018 | 0.022 | 0.006 | 0.031 | 12/15 | f0:+0.033 / f1:+0.020 / f2:+0.002 | 3 |

### Every run: before (pre) / after (post) Stage III

| run | pre_acc | pre_bal_acc | pre_split_vote_acc | pre_unanimous_acc | post_acc | post_bal_acc | post_split_vote_acc | post_unanimous_acc |
|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.832 | 0.806 | 0.680 | 0.898 | 0.848 | 0.832 | 0.709 | 0.909 |
| f0s0_hsrl_no_stage1 | 0.763 | 0.704 | 0.547 | 0.858 | 0.653 | 0.701 | 0.690 | 0.637 |
| f0s0_hsrl_no_t2 | 0.775 | 0.718 | 0.571 | 0.864 | 0.785 | 0.736 | 0.581 | 0.875 |
| f0s1_hsrl | 0.785 | 0.762 | 0.606 | 0.864 | 0.808 | 0.785 | 0.655 | 0.875 |
| f0s1_hsrl_no_stage1 | 0.730 | 0.663 | 0.493 | 0.834 | 0.650 | 0.692 | 0.660 | 0.646 |
| f0s1_hsrl_no_t2 | 0.793 | 0.757 | 0.606 | 0.875 | 0.817 | 0.785 | 0.660 | 0.885 |
| f0s2_hsrl | 0.809 | 0.781 | 0.655 | 0.877 | 0.844 | 0.823 | 0.714 | 0.901 |
| f0s2_hsrl_no_stage1 | 0.775 | 0.733 | 0.586 | 0.858 | 0.709 | 0.738 | 0.685 | 0.719 |
| f0s2_hsrl_no_t2 | 0.817 | 0.786 | 0.650 | 0.890 | 0.820 | 0.790 | 0.650 | 0.894 |
| f0s3_hsrl | 0.805 | 0.766 | 0.626 | 0.883 | 0.817 | 0.780 | 0.630 | 0.898 |
| f0s3_hsrl_no_stage1 | 0.760 | 0.714 | 0.586 | 0.836 | 0.647 | 0.693 | 0.655 | 0.644 |
| f0s3_hsrl_no_t2 | 0.814 | 0.788 | 0.675 | 0.875 | 0.836 | 0.822 | 0.719 | 0.888 |
| f0s4_hsrl | 0.800 | 0.776 | 0.640 | 0.870 | 0.827 | 0.807 | 0.700 | 0.883 |
| f0s4_hsrl_no_stage1 | 0.769 | 0.726 | 0.581 | 0.851 | 0.694 | 0.718 | 0.655 | 0.711 |
| f0s4_hsrl_no_t2 | 0.817 | 0.791 | 0.645 | 0.892 | 0.830 | 0.819 | 0.700 | 0.888 |
| f1s0_hsrl | 0.823 | 0.818 | 0.667 | 0.881 | 0.839 | 0.829 | 0.687 | 0.896 |
| f1s0_hsrl_no_stage1 | 0.738 | 0.741 | 0.627 | 0.779 | 0.573 | 0.621 | 0.657 | 0.542 |
| f1s0_hsrl_no_t2 | 0.799 | 0.775 | 0.607 | 0.870 | 0.824 | 0.808 | 0.627 | 0.898 |
| f1s1_hsrl | 0.826 | 0.813 | 0.657 | 0.889 | 0.831 | 0.827 | 0.677 | 0.889 |
| f1s1_hsrl_no_stage1 | 0.754 | 0.707 | 0.582 | 0.818 | 0.670 | 0.689 | 0.617 | 0.690 |
| f1s1_hsrl_no_t2 | 0.826 | 0.817 | 0.667 | 0.885 | 0.831 | 0.822 | 0.682 | 0.887 |
| f1s2_hsrl | 0.820 | 0.800 | 0.642 | 0.887 | 0.838 | 0.821 | 0.667 | 0.902 |
| f1s2_hsrl_no_stage1 | 0.781 | 0.748 | 0.617 | 0.842 | 0.672 | 0.682 | 0.627 | 0.688 |
| f1s2_hsrl_no_t2 | 0.816 | 0.800 | 0.672 | 0.870 | 0.827 | 0.817 | 0.697 | 0.876 |
| f1s3_hsrl | 0.800 | 0.811 | 0.662 | 0.852 | 0.828 | 0.831 | 0.687 | 0.881 |
| f1s3_hsrl_no_stage1 | 0.754 | 0.731 | 0.587 | 0.816 | 0.700 | 0.710 | 0.662 | 0.714 |
| f1s3_hsrl_no_t2 | 0.811 | 0.806 | 0.612 | 0.885 | 0.822 | 0.819 | 0.647 | 0.887 |
| f1s4_hsrl | 0.812 | 0.807 | 0.687 | 0.859 | 0.832 | 0.825 | 0.707 | 0.879 |
| f1s4_hsrl_no_stage1 | 0.732 | 0.712 | 0.582 | 0.788 | 0.692 | 0.686 | 0.577 | 0.735 |
| f1s4_hsrl_no_t2 | 0.828 | 0.819 | 0.692 | 0.879 | 0.854 | 0.844 | 0.697 | 0.913 |
| f2s0_hsrl | 0.789 | 0.774 | 0.633 | 0.848 | 0.814 | 0.808 | 0.669 | 0.868 |
| f2s0_hsrl_no_stage1 | 0.700 | 0.653 | 0.420 | 0.806 | 0.650 | 0.692 | 0.657 | 0.647 |
| f2s0_hsrl_no_t2 | 0.797 | 0.789 | 0.669 | 0.846 | 0.809 | 0.800 | 0.657 | 0.866 |
| f2s1_hsrl | 0.778 | 0.774 | 0.627 | 0.835 | 0.799 | 0.788 | 0.639 | 0.859 |
| f2s1_hsrl_no_stage1 | 0.716 | 0.666 | 0.456 | 0.815 | 0.637 | 0.689 | 0.698 | 0.614 |
| f2s1_hsrl_no_t2 | 0.794 | 0.783 | 0.651 | 0.848 | 0.796 | 0.783 | 0.627 | 0.859 |
| f2s2_hsrl | 0.801 | 0.784 | 0.627 | 0.866 | 0.802 | 0.785 | 0.604 | 0.877 |
| f2s2_hsrl_no_stage1 | 0.718 | 0.677 | 0.438 | 0.824 | 0.651 | 0.700 | 0.680 | 0.641 |
| f2s2_hsrl_no_t2 | 0.814 | 0.795 | 0.639 | 0.879 | 0.815 | 0.802 | 0.657 | 0.875 |
| f2s3_hsrl | 0.823 | 0.822 | 0.692 | 0.873 | 0.823 | 0.826 | 0.698 | 0.871 |
| f2s3_hsrl_no_stage1 | 0.705 | 0.663 | 0.450 | 0.801 | 0.666 | 0.708 | 0.657 | 0.670 |
| f2s3_hsrl_no_t2 | 0.814 | 0.817 | 0.692 | 0.859 | 0.831 | 0.837 | 0.704 | 0.879 |
| f2s4_hsrl | 0.794 | 0.775 | 0.639 | 0.853 | 0.807 | 0.789 | 0.639 | 0.871 |
| f2s4_hsrl_no_stage1 | 0.718 | 0.659 | 0.438 | 0.824 | 0.682 | 0.718 | 0.680 | 0.683 |
| f2s4_hsrl_no_t2 | 0.812 | 0.797 | 0.663 | 0.868 | 0.823 | 0.809 | 0.680 | 0.877 |

## 4. Stage III pseudo-labels (vs hidden majority labels)

| config | runs | coverage | precision | prec_unanimous | prec_split | min_coverage |
|---|---|---|---|---|---|---|
| hsrl | 15 | 0.604 ± 0.049 | 0.944 ± 0.009 | 0.969 ± 0.012 | 0.839 ± 0.016 | 0.536 |
| hsrl_no_stage1 | 15 | 0.087 ± 0.056 | 0.987 ± 0.008 | 0.993 ± 0.007 | nan ± nan | 0.009 |
| hsrl_no_t2 | 15 | 0.627 ± 0.047 | 0.939 ± 0.015 | 0.968 ± 0.014 | 0.822 ± 0.030 | 0.545 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl | 15 | 30 | 0/15 | 0/15 | - | 0.242 ± 0.079 | 1.690 ± 0.226 | 0.768 ± 0.043 | 0.15/0.38/0.02 |
| hsrl_no_t2 | 15 | 30 | 0/15 | 0/15 | - | 0.279 ± 0.079 | 1.711 ± 0.189 | 0.759 ± 0.044 | 0.05/0.60/0.01 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.743 | 0.146 | 17 | None | None | 1.234 | 0.809 |
| f0s0_hsrl_no_t2 | 0.743 | 0.174 | 11 | None | None | 1.076 | 0.664 |
| f0s1_hsrl | 0.690 | 0.197 | 13 | None | None | 1.626 | 0.774 |
| f0s1_hsrl_no_t2 | 0.690 | 0.219 | 9 | None | None | 1.587 | 0.769 |
| f0s2_hsrl | 0.627 | 0.155 | 17 | None | None | 1.418 | 0.769 |
| f0s2_hsrl_no_t2 | 0.627 | 0.184 | 10 | None | None | 1.694 | 0.815 |
| f0s3_hsrl | 0.784 | 0.162 | 16 | None | None | 1.209 | 0.687 |
| f0s3_hsrl_no_t2 | 0.784 | 0.192 | 10 | None | None | 1.710 | 0.833 |
| f0s4_hsrl | 0.810 | 0.190 | 14 | None | None | 1.797 | 0.844 |
| f0s4_hsrl_no_t2 | 0.810 | 0.254 | 9 | None | None | 1.758 | 0.809 |
| f1s0_hsrl | 0.712 | 0.249 | 10 | None | None | 1.898 | 0.794 |
| f1s0_hsrl_no_t2 | 0.712 | 0.280 | 8 | None | None | 1.837 | 0.774 |
| f1s1_hsrl | 0.674 | 0.224 | 11 | None | None | 1.704 | 0.743 |
| f1s1_hsrl_no_t2 | 0.674 | 0.275 | 8 | None | None | 1.805 | 0.744 |
| f1s2_hsrl | 0.603 | 0.212 | 11 | None | None | 1.805 | 0.708 |
| f1s2_hsrl_no_t2 | 0.603 | 0.244 | 8 | None | None | 1.656 | 0.722 |
| f1s3_hsrl | 0.732 | 0.297 | 10 | None | None | 1.911 | 0.832 |
| f1s3_hsrl_no_t2 | 0.732 | 0.324 | 8 | None | None | 1.778 | 0.714 |
| f1s4_hsrl | 0.775 | 0.278 | 10 | None | None | 1.782 | 0.751 |
| f1s4_hsrl_no_t2 | 0.775 | 0.345 | 7 | None | None | 1.827 | 0.772 |
| f2s0_hsrl | 0.767 | 0.448 | 7 | None | None | 1.758 | 0.733 |
| f2s0_hsrl_no_t2 | 0.767 | 0.466 | 6 | None | None | 1.771 | 0.762 |
| f2s1_hsrl | 0.721 | 0.292 | 9 | None | None | 1.813 | 0.773 |
| f2s1_hsrl_no_t2 | 0.721 | 0.341 | 6 | None | None | 1.807 | 0.773 |
| f2s2_hsrl | 0.665 | 0.185 | 13 | None | None | 1.833 | 0.766 |
| f2s2_hsrl_no_t2 | 0.665 | 0.220 | 10 | None | None | 1.765 | 0.745 |
| f2s3_hsrl | 0.806 | 0.291 | 9 | None | None | 1.864 | 0.795 |
| f2s3_hsrl_no_t2 | 0.806 | 0.323 | 7 | None | None | 1.799 | 0.778 |
| f2s4_hsrl | 0.813 | 0.301 | 10 | None | None | 1.695 | 0.736 |
| f2s4_hsrl_no_t2 | 0.813 | 0.345 | 7 | None | None | 1.804 | 0.716 |
