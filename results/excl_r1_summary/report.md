# Aggregate over results/excl_r1

Runs: 60; folds [0, 1, 2]; seeds [0, 1, 2, 3, 4]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl | 15 | 0.794 ± 0.018 | 0.767 ± 0.025 | 0.773 ± 0.021 | 0.863 ± 0.016 | 0.160 ± 0.024 | 0.832 ± 0.010 | 0.623 ± 0.058 |
| hsrl_soft | 15 | 0.789 ± 0.016 | 0.764 ± 0.027 | 0.767 ± 0.021 | 0.860 ± 0.020 | 0.162 ± 0.023 | 0.826 ± 0.007 | 0.620 ± 0.057 |
| supervised | 15 | 0.779 ± 0.024 | 0.762 ± 0.025 | 0.762 ± 0.024 | 0.846 ± 0.023 | 0.179 ± 0.024 | 0.819 ± 0.023 | 0.598 ± 0.048 |
| supervised_soft | 15 | 0.791 ± 0.022 | 0.776 ± 0.031 | 0.775 ± 0.025 | 0.868 ± 0.023 | 0.152 ± 0.018 | 0.833 ± 0.016 | 0.596 ± 0.054 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl | 0 | 5 | 0.775 ± 0.009 | 0.744 ± 0.014 | 0.844 ± 0.012 | 0.550 ± 0.012 |
| hsrl_soft | 0 | 5 | 0.770 ± 0.012 | 0.735 ± 0.015 | 0.836 ± 0.013 | 0.546 ± 0.009 |
| supervised | 0 | 5 | 0.766 ± 0.006 | 0.737 ± 0.009 | 0.825 ± 0.005 | 0.541 ± 0.019 |
| supervised_soft | 0 | 5 | 0.770 ± 0.006 | 0.741 ± 0.007 | 0.846 ± 0.006 | 0.531 ± 0.017 |
| hsrl | 1 | 5 | 0.813 ± 0.010 | 0.792 ± 0.020 | 0.875 ± 0.009 | 0.681 ± 0.013 |
| hsrl_soft | 1 | 5 | 0.801 ± 0.004 | 0.792 ± 0.013 | 0.874 ± 0.012 | 0.675 ± 0.009 |
| supervised | 1 | 5 | 0.795 ± 0.027 | 0.785 ± 0.022 | 0.864 ± 0.026 | 0.640 ± 0.031 |
| supervised_soft | 1 | 5 | 0.814 ± 0.016 | 0.813 ± 0.007 | 0.896 ± 0.009 | 0.644 ± 0.026 |
| hsrl | 2 | 5 | 0.795 ± 0.002 | 0.764 ± 0.012 | 0.868 ± 0.004 | 0.637 ± 0.016 |
| hsrl_soft | 2 | 5 | 0.796 ± 0.002 | 0.766 ± 0.010 | 0.871 ± 0.005 | 0.640 ± 0.010 |
| supervised | 2 | 5 | 0.778 ± 0.026 | 0.763 ± 0.011 | 0.849 ± 0.015 | 0.613 ± 0.013 |
| supervised_soft | 2 | 5 | 0.789 ± 0.013 | 0.775 ± 0.012 | 0.862 ± 0.011 | 0.612 ± 0.025 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| supervised_soft − supervised | overall | acc | 15 | 0.012 | 0.017 | 0.002 | 0.021 | 12/15 | f0:+0.005 / f1:+0.019 / f2:+0.011 | 3 |
| supervised_soft − supervised | overall | bal_acc | 15 | 0.015 | 0.015 | 0.006 | 0.023 | 14/15 | f0:+0.004 / f1:+0.028 / f2:+0.012 | 3 |
| supervised_soft − supervised | overall | auroc | 15 | 0.022 | 0.016 | 0.014 | 0.031 | 14/15 | f0:+0.021 / f1:+0.032 / f2:+0.014 | 3 |
| supervised_soft − supervised | overall | brier | 15 | -0.027 | 0.013 | -0.034 | -0.020 | 15/15 | f0:-0.029 / f1:-0.024 / f2:-0.028 | 3 |
| supervised_soft − supervised | split_vote | acc | 15 | -0.002 | 0.019 | -0.012 | 0.008 | 7/15 | f0:-0.010 / f1:+0.005 / f2:-0.001 | 2 |
| hsrl_soft − hsrl | overall | acc | 15 | -0.005 | 0.008 | -0.010 | -0.001 | 4/15 | f0:-0.005 / f1:-0.012 / f2:+0.001 | 2 |
| hsrl_soft − hsrl | overall | bal_acc | 15 | -0.003 | 0.009 | -0.007 | 0.002 | 6/15 | f0:-0.009 / f1:+0.000 / f2:+0.002 | 1 |
| hsrl_soft − hsrl | overall | auroc | 15 | -0.002 | 0.007 | -0.006 | 0.001 | 7/15 | f0:-0.008 / f1:-0.001 / f2:+0.003 | 2 |
| hsrl_soft − hsrl | overall | brier | 15 | 0.002 | 0.006 | -0.001 | 0.005 | 7/15 | f0:+0.003 / f1:+0.005 / f2:-0.003 | 2 |
| hsrl_soft − hsrl | split_vote | acc | 15 | -0.003 | 0.010 | -0.009 | 0.003 | 6/15 | f0:-0.005 / f1:-0.006 / f2:+0.002 | 2 |
| hsrl − supervised | overall | acc | 15 | 0.015 | 0.023 | 0.002 | 0.027 | 11/15 | f0:+0.009 / f1:+0.018 / f2:+0.017 | 3 |
| hsrl − supervised | overall | bal_acc | 15 | 0.005 | 0.021 | -0.007 | 0.017 | 10/15 | f0:+0.007 / f1:+0.007 / f2:+0.001 | 3 |
| hsrl − supervised | overall | auroc | 15 | 0.017 | 0.020 | 0.006 | 0.028 | 13/15 | f0:+0.019 / f1:+0.012 / f2:+0.020 | 3 |
| hsrl − supervised | overall | brier | 15 | -0.018 | 0.018 | -0.028 | -0.008 | 14/15 | f0:-0.012 / f1:-0.024 / f2:-0.019 | 3 |
| hsrl − supervised | split_vote | acc | 15 | 0.025 | 0.025 | 0.011 | 0.038 | 13/15 | f0:+0.009 / f1:+0.041 / f2:+0.024 | 3 |
| hsrl_soft − supervised_soft | overall | acc | 15 | -0.002 | 0.016 | -0.011 | 0.006 | 7/15 | f0:-0.001 / f1:-0.013 / f2:+0.007 | 2 |
| hsrl_soft − supervised_soft | overall | bal_acc | 15 | -0.012 | 0.015 | -0.020 | -0.004 | 2/15 | f0:-0.006 / f1:-0.020 / f2:-0.009 | 3 |
| hsrl_soft − supervised_soft | overall | auroc | 15 | -0.008 | 0.018 | -0.018 | 0.003 | 7/15 | f0:-0.010 / f1:-0.022 / f2:+0.009 | 2 |
| hsrl_soft − supervised_soft | overall | brier | 15 | 0.011 | 0.013 | 0.004 | 0.018 | 3/15 | f0:+0.020 / f1:+0.006 / f2:+0.006 | 3 |
| hsrl_soft − supervised_soft | split_vote | acc | 15 | 0.024 | 0.021 | 0.012 | 0.036 | 15/15 | f0:+0.014 / f1:+0.031 / f2:+0.027 | 3 |

## 3. Effect of Stage III (after − before, paired within run)

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl[final] − hsrl[before_stage3] | overall | acc | 15 | 0.025 | 0.018 | 0.015 | 0.035 | 14/15 | f0:+0.006 / f1:+0.046 / f2:+0.023 | 3 |
| hsrl[final] − hsrl[before_stage3] | overall | bal_acc | 15 | 0.025 | 0.027 | 0.010 | 0.040 | 13/15 | f0:+0.002 / f1:+0.060 / f2:+0.014 | 3 |
| hsrl[final] − hsrl[before_stage3] | overall | auroc | 15 | 0.023 | 0.020 | 0.012 | 0.034 | 14/15 | f0:+0.001 / f1:+0.047 / f2:+0.022 | 3 |
| hsrl[final] − hsrl[before_stage3] | unanimous | acc | 15 | 0.028 | 0.018 | 0.018 | 0.039 | 14/15 | f0:+0.008 / f1:+0.049 / f2:+0.029 | 3 |
| hsrl[final] − hsrl[before_stage3] | split_vote | acc | 15 | 0.009 | 0.020 | -0.002 | 0.021 | 7/15 | f0:+0.000 / f1:+0.035 / f2:-0.007 | 2 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | acc | 15 | 0.021 | 0.013 | 0.014 | 0.029 | 14/15 | f0:+0.006 / f1:+0.031 / f2:+0.026 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | bal_acc | 15 | 0.023 | 0.024 | 0.010 | 0.036 | 13/15 | f0:+0.003 / f1:+0.052 / f2:+0.014 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | auroc | 15 | 0.019 | 0.022 | 0.007 | 0.032 | 11/15 | f0:-0.008 / f1:+0.042 / f2:+0.024 | 2 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | unanimous | acc | 15 | 0.024 | 0.014 | 0.016 | 0.031 | 15/15 | f0:+0.008 / f1:+0.032 / f2:+0.031 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | split_vote | acc | 15 | 0.009 | 0.018 | -0.001 | 0.019 | 8/15 | f0:+0.001 / f1:+0.029 / f2:-0.002 | 2 |

### Every run: before (pre) / after (post) Stage III

| run | pre_acc | pre_bal_acc | pre_split_vote_acc | pre_unanimous_acc | post_acc | post_bal_acc | post_split_vote_acc | post_unanimous_acc |
|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.756 | 0.725 | 0.520 | 0.815 | 0.767 | 0.731 | 0.537 | 0.825 |
| f0s0_hsrl_soft | 0.748 | 0.709 | 0.539 | 0.800 | 0.760 | 0.721 | 0.539 | 0.815 |
| f0s1_hsrl | 0.760 | 0.736 | 0.553 | 0.812 | 0.767 | 0.736 | 0.550 | 0.821 |
| f0s1_hsrl_soft | 0.754 | 0.723 | 0.544 | 0.807 | 0.756 | 0.717 | 0.535 | 0.811 |
| f0s2_hsrl | 0.771 | 0.745 | 0.548 | 0.827 | 0.780 | 0.753 | 0.555 | 0.836 |
| f0s2_hsrl_soft | 0.765 | 0.734 | 0.531 | 0.824 | 0.781 | 0.748 | 0.548 | 0.839 |
| f0s3_hsrl | 0.779 | 0.755 | 0.572 | 0.830 | 0.789 | 0.764 | 0.568 | 0.844 |
| f0s3_hsrl_soft | 0.776 | 0.749 | 0.555 | 0.831 | 0.780 | 0.750 | 0.559 | 0.835 |
| f0s4_hsrl | 0.775 | 0.751 | 0.557 | 0.829 | 0.770 | 0.738 | 0.542 | 0.827 |
| f0s4_hsrl_soft | 0.772 | 0.743 | 0.553 | 0.827 | 0.772 | 0.738 | 0.546 | 0.828 |
| f1s0_hsrl | 0.774 | 0.740 | 0.638 | 0.801 | 0.811 | 0.796 | 0.670 | 0.841 |
| f1s0_hsrl_soft | 0.777 | 0.742 | 0.631 | 0.807 | 0.803 | 0.797 | 0.663 | 0.831 |
| f1s1_hsrl | 0.750 | 0.690 | 0.629 | 0.774 | 0.802 | 0.763 | 0.667 | 0.830 |
| f1s1_hsrl_soft | 0.749 | 0.698 | 0.620 | 0.776 | 0.798 | 0.770 | 0.667 | 0.824 |
| f1s2_hsrl | 0.770 | 0.752 | 0.654 | 0.794 | 0.817 | 0.795 | 0.683 | 0.844 |
| f1s2_hsrl_soft | 0.781 | 0.757 | 0.670 | 0.804 | 0.806 | 0.797 | 0.681 | 0.832 |
| f1s3_hsrl | 0.776 | 0.756 | 0.663 | 0.800 | 0.829 | 0.819 | 0.701 | 0.855 |
| f1s3_hsrl_soft | 0.774 | 0.768 | 0.656 | 0.799 | 0.803 | 0.805 | 0.683 | 0.828 |
| f1s4_hsrl | 0.765 | 0.723 | 0.647 | 0.789 | 0.808 | 0.788 | 0.683 | 0.833 |
| f1s4_hsrl_soft | 0.766 | 0.738 | 0.654 | 0.789 | 0.795 | 0.792 | 0.681 | 0.819 |
| f2s0_hsrl | 0.780 | 0.747 | 0.653 | 0.803 | 0.797 | 0.764 | 0.647 | 0.824 |
| f2s0_hsrl_soft | 0.780 | 0.750 | 0.659 | 0.802 | 0.795 | 0.758 | 0.653 | 0.821 |
| f2s1_hsrl | 0.771 | 0.749 | 0.636 | 0.796 | 0.794 | 0.763 | 0.630 | 0.824 |
| f2s1_hsrl_soft | 0.771 | 0.753 | 0.644 | 0.794 | 0.794 | 0.772 | 0.633 | 0.823 |
| f2s2_hsrl | 0.770 | 0.754 | 0.656 | 0.791 | 0.796 | 0.758 | 0.653 | 0.822 |
| f2s2_hsrl_soft | 0.761 | 0.750 | 0.636 | 0.784 | 0.795 | 0.757 | 0.633 | 0.825 |
| f2s3_hsrl | 0.772 | 0.764 | 0.647 | 0.795 | 0.793 | 0.783 | 0.644 | 0.821 |
| f2s3_hsrl_soft | 0.766 | 0.760 | 0.627 | 0.792 | 0.799 | 0.780 | 0.647 | 0.827 |
| f2s4_hsrl | 0.766 | 0.738 | 0.630 | 0.791 | 0.796 | 0.753 | 0.612 | 0.830 |
| f2s4_hsrl_soft | 0.771 | 0.749 | 0.644 | 0.794 | 0.796 | 0.763 | 0.633 | 0.826 |

## 4. Stage III pseudo-labels (vs hidden majority labels)

| config | runs | coverage | precision | prec_unanimous | prec_split | min_coverage |
|---|---|---|---|---|---|---|
| hsrl | 15 | 0.549 ± 0.231 | 0.923 ± 0.010 | 0.956 ± 0.008 | 0.725 ± 0.022 | 0.221 |
| hsrl_soft | 15 | 0.478 ± 0.182 | 0.938 ± 0.007 | 0.968 ± 0.005 | 0.734 ± 0.021 | 0.215 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl | 15 | 30 | 15/15 | 6/15 | 21 22 23 23 24 29 | 0.037 ± 0.017 | 0.551 ± 0.676 | 0.773 ± 0.057 | 0.78/0.78/0.67 |
| hsrl_soft | 15 | 30 | 15/15 | 6/15 | 21 22 23 23 24 29 | 0.037 ± 0.017 | 0.551 ± 0.676 | 0.773 ± 0.057 | 0.78/0.78/0.67 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.732 | 0.060 | 13 | 10 | 21.000 | 1.327 | 0.806 |
| f0s0_hsrl_soft | 0.732 | 0.060 | 13 | 10 | 21.000 | 1.327 | 0.806 |
| f0s1_hsrl | 0.688 | 0.064 | 14 | 12 | 22.000 | 1.627 | 0.802 |
| f0s1_hsrl_soft | 0.688 | 0.064 | 14 | 12 | 22.000 | 1.627 | 0.802 |
| f0s2_hsrl | 0.602 | 0.047 | 16 | 10 | 23.000 | 1.281 | 0.698 |
| f0s2_hsrl_soft | 0.602 | 0.047 | 16 | 10 | 23.000 | 1.281 | 0.698 |
| f0s3_hsrl | 0.781 | 0.064 | 15 | 11 | 23.000 | 1.451 | 0.741 |
| f0s3_hsrl_soft | 0.781 | 0.064 | 15 | 11 | 23.000 | 1.451 | 0.741 |
| f0s4_hsrl | 0.807 | 0.054 | 16 | 8 | 24.000 | 1.439 | 0.812 |
| f0s4_hsrl_soft | 0.807 | 0.054 | 16 | 8 | 24.000 | 1.439 | 0.812 |
| f1s0_hsrl | 0.710 | 0.018 | 29 | 7 | nan | 0.018 | 0.694 |
| f1s0_hsrl_soft | 0.710 | 0.018 | 29 | 7 | nan | 0.018 | 0.694 |
| f1s1_hsrl | 0.658 | 0.018 | 29 | 8 | nan | 0.018 | 0.720 |
| f1s1_hsrl_soft | 0.658 | 0.018 | 29 | 8 | nan | 0.018 | 0.720 |
| f1s2_hsrl | 0.575 | 0.018 | 29 | 9 | nan | 0.018 | 0.715 |
| f1s2_hsrl_soft | 0.575 | 0.018 | 29 | 9 | nan | 0.018 | 0.715 |
| f1s3_hsrl | 0.756 | 0.021 | 29 | 8 | nan | 0.021 | 0.726 |
| f1s3_hsrl_soft | 0.756 | 0.021 | 29 | 8 | nan | 0.021 | 0.726 |
| f1s4_hsrl | 0.755 | 0.017 | 29 | 6 | nan | 0.017 | 0.724 |
| f1s4_hsrl_soft | 0.755 | 0.017 | 29 | 6 | nan | 0.017 | 0.724 |
| f2s0_hsrl | 0.758 | 0.035 | 20 | 7 | nan | 0.073 | 0.816 |
| f2s0_hsrl_soft | 0.758 | 0.035 | 20 | 7 | nan | 0.073 | 0.816 |
| f2s1_hsrl | 0.709 | 0.030 | 23 | 8 | nan | 0.038 | 0.844 |
| f2s1_hsrl_soft | 0.709 | 0.030 | 23 | 8 | nan | 0.038 | 0.844 |
| f2s2_hsrl | 0.616 | 0.032 | 22 | 9 | nan | 0.041 | 0.838 |
| f2s2_hsrl_soft | 0.616 | 0.032 | 22 | 9 | nan | 0.041 | 0.838 |
| f2s3_hsrl | 0.808 | 0.043 | 20 | 8 | 29.000 | 0.846 | 0.831 |
| f2s3_hsrl_soft | 0.808 | 0.043 | 20 | 8 | 29.000 | 0.846 | 0.831 |
| f2s4_hsrl | 0.800 | 0.036 | 25 | 7 | nan | 0.054 | 0.834 |
| f2s4_hsrl_soft | 0.800 | 0.036 | 25 | 7 | nan | 0.054 | 0.834 |
