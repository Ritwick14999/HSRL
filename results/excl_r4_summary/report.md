# Aggregate over results/excl_r4

Runs: 60; folds [0, 1, 2]; seeds [0, 1, 2, 3, 4]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl | 15 | 0.797 ± 0.035 | 0.760 ± 0.043 | 0.769 ± 0.042 | 0.872 ± 0.031 | 0.159 ± 0.032 | 0.870 ± 0.018 | 0.611 ± 0.059 |
| hsrl_soft | 15 | 0.793 ± 0.036 | 0.753 ± 0.047 | 0.762 ± 0.047 | 0.868 ± 0.031 | 0.161 ± 0.031 | 0.867 ± 0.018 | 0.601 ± 0.072 |
| supervised | 15 | 0.797 ± 0.032 | 0.772 ± 0.038 | 0.776 ± 0.035 | 0.863 ± 0.032 | 0.167 ± 0.029 | 0.863 ± 0.021 | 0.624 ± 0.041 |
| supervised_soft | 15 | 0.807 ± 0.031 | 0.778 ± 0.039 | 0.785 ± 0.036 | 0.878 ± 0.030 | 0.139 ± 0.023 | 0.876 ± 0.018 | 0.630 ± 0.047 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl | 0 | 5 | 0.773 ± 0.009 | 0.737 ± 0.011 | 0.845 ± 0.010 | 0.586 ± 0.018 |
| hsrl_soft | 0 | 5 | 0.775 ± 0.009 | 0.739 ± 0.014 | 0.841 ± 0.009 | 0.587 ± 0.019 |
| supervised | 0 | 5 | 0.762 ± 0.007 | 0.737 ± 0.013 | 0.827 ± 0.009 | 0.591 ± 0.023 |
| supervised_soft | 0 | 5 | 0.784 ± 0.007 | 0.754 ± 0.011 | 0.860 ± 0.006 | 0.605 ± 0.014 |
| hsrl | 1 | 5 | 0.843 ± 0.009 | 0.817 ± 0.011 | 0.912 ± 0.007 | 0.686 ± 0.014 |
| hsrl_soft | 1 | 5 | 0.839 ± 0.010 | 0.810 ± 0.014 | 0.908 ± 0.008 | 0.685 ± 0.018 |
| supervised | 1 | 5 | 0.838 ± 0.005 | 0.820 ± 0.013 | 0.901 ± 0.010 | 0.670 ± 0.025 |
| supervised_soft | 1 | 5 | 0.849 ± 0.010 | 0.829 ± 0.014 | 0.918 ± 0.008 | 0.692 ± 0.016 |
| hsrl | 2 | 5 | 0.775 ± 0.010 | 0.727 ± 0.016 | 0.860 ± 0.006 | 0.559 ± 0.023 |
| hsrl_soft | 2 | 5 | 0.765 ± 0.016 | 0.709 ± 0.029 | 0.855 ± 0.008 | 0.531 ± 0.047 |
| supervised | 2 | 5 | 0.791 ± 0.004 | 0.758 ± 0.010 | 0.860 ± 0.007 | 0.613 ± 0.022 |
| supervised_soft | 2 | 5 | 0.789 ± 0.004 | 0.750 ± 0.004 | 0.857 ± 0.007 | 0.593 ± 0.006 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| supervised_soft − supervised | overall | acc | 15 | 0.011 | 0.013 | 0.004 | 0.018 | 13/15 | f0:+0.022 / f1:+0.012 / f2:-0.002 | 2 |
| supervised_soft − supervised | overall | bal_acc | 15 | 0.006 | 0.016 | -0.003 | 0.015 | 9/15 | f0:+0.017 / f1:+0.009 / f2:-0.008 | 2 |
| supervised_soft − supervised | overall | auroc | 15 | 0.016 | 0.017 | 0.007 | 0.025 | 12/15 | f0:+0.033 / f1:+0.017 / f2:-0.003 | 2 |
| supervised_soft − supervised | overall | brier | 15 | -0.028 | 0.011 | -0.034 | -0.021 | 15/15 | f0:-0.042 / f1:-0.021 / f2:-0.021 | 3 |
| supervised_soft − supervised | split_vote | acc | 15 | 0.005 | 0.031 | -0.012 | 0.023 | 8/15 | f0:+0.014 / f1:+0.022 / f2:-0.020 | 2 |
| hsrl_soft − hsrl | overall | acc | 15 | -0.004 | 0.012 | -0.011 | 0.002 | 5/15 | f0:+0.002 / f1:-0.005 / f2:-0.011 | 2 |
| hsrl_soft − hsrl | overall | bal_acc | 15 | -0.008 | 0.022 | -0.020 | 0.005 | 5/15 | f0:+0.002 / f1:-0.007 / f2:-0.018 | 2 |
| hsrl_soft − hsrl | overall | auroc | 15 | -0.004 | 0.006 | -0.007 | -0.001 | 4/15 | f0:-0.003 / f1:-0.004 / f2:-0.005 | 3 |
| hsrl_soft − hsrl | overall | brier | 15 | 0.002 | 0.010 | -0.004 | 0.008 | 5/15 | f0:-0.005 / f1:+0.003 / f2:+0.007 | 2 |
| hsrl_soft − hsrl | split_vote | acc | 15 | -0.009 | 0.036 | -0.029 | 0.011 | 5/15 | f0:+0.001 / f1:-0.001 / f2:-0.028 | 2 |

## 3. Effect of Stage III (after − before, paired within run)

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl[final] − hsrl[before_stage3] | overall | acc | 15 | 0.019 | 0.008 | 0.014 | 0.023 | 15/15 | f0:+0.010 / f1:+0.024 / f2:+0.021 | 3 |
| hsrl[final] − hsrl[before_stage3] | overall | bal_acc | 15 | 0.014 | 0.011 | 0.008 | 0.020 | 13/15 | f0:+0.004 / f1:+0.019 / f2:+0.018 | 3 |
| hsrl[final] − hsrl[before_stage3] | overall | auroc | 15 | 0.015 | 0.010 | 0.010 | 0.020 | 14/15 | f0:+0.005 / f1:+0.021 / f2:+0.020 | 3 |
| hsrl[final] − hsrl[before_stage3] | unanimous | acc | 15 | 0.023 | 0.011 | 0.016 | 0.029 | 15/15 | f0:+0.011 / f1:+0.031 / f2:+0.026 | 3 |
| hsrl[final] − hsrl[before_stage3] | split_vote | acc | 15 | 0.006 | 0.014 | -0.002 | 0.014 | 10/15 | f0:+0.010 / f1:+0.002 / f2:+0.007 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | acc | 15 | 0.015 | 0.012 | 0.008 | 0.022 | 13/15 | f0:+0.014 / f1:+0.019 / f2:+0.012 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | bal_acc | 15 | 0.015 | 0.023 | 0.003 | 0.028 | 13/15 | f0:+0.017 / f1:+0.023 / f2:+0.006 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | overall | auroc | 15 | 0.011 | 0.011 | 0.005 | 0.017 | 12/15 | f0:-0.001 / f1:+0.017 / f2:+0.017 | 2 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | unanimous | acc | 15 | 0.017 | 0.010 | 0.011 | 0.023 | 14/15 | f0:+0.009 / f1:+0.021 / f2:+0.021 | 3 |
| hsrl_soft[final] − hsrl_soft[before_stage3] | split_vote | acc | 15 | 0.009 | 0.033 | -0.009 | 0.027 | 11/15 | f0:+0.023 / f1:+0.015 / f2:-0.011 | 2 |

### Every run: before (pre) / after (post) Stage III

| run | pre_acc | pre_bal_acc | pre_split_vote_acc | pre_unanimous_acc | post_acc | post_bal_acc | post_split_vote_acc | post_unanimous_acc |
|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.770 | 0.747 | 0.583 | 0.859 | 0.777 | 0.749 | 0.605 | 0.860 |
| f0s0_hsrl_soft | 0.768 | 0.736 | 0.573 | 0.862 | 0.764 | 0.723 | 0.560 | 0.862 |
| f0s1_hsrl | 0.754 | 0.720 | 0.559 | 0.846 | 0.760 | 0.720 | 0.560 | 0.855 |
| f0s1_hsrl_soft | 0.753 | 0.710 | 0.544 | 0.853 | 0.779 | 0.749 | 0.606 | 0.861 |
| f0s2_hsrl | 0.764 | 0.737 | 0.586 | 0.849 | 0.770 | 0.736 | 0.576 | 0.862 |
| f0s2_hsrl_soft | 0.768 | 0.732 | 0.580 | 0.858 | 0.781 | 0.751 | 0.596 | 0.869 |
| f0s3_hsrl | 0.758 | 0.725 | 0.573 | 0.846 | 0.775 | 0.735 | 0.592 | 0.862 |
| f0s3_hsrl_soft | 0.757 | 0.716 | 0.559 | 0.852 | 0.766 | 0.725 | 0.576 | 0.857 |
| f0s4_hsrl | 0.768 | 0.736 | 0.581 | 0.857 | 0.783 | 0.746 | 0.598 | 0.871 |
| f0s4_hsrl_soft | 0.760 | 0.718 | 0.567 | 0.852 | 0.785 | 0.747 | 0.598 | 0.875 |
| f1s0_hsrl | 0.835 | 0.816 | 0.693 | 0.880 | 0.855 | 0.824 | 0.691 | 0.906 |
| f1s0_hsrl_soft | 0.833 | 0.798 | 0.674 | 0.883 | 0.854 | 0.820 | 0.699 | 0.902 |
| f1s1_hsrl | 0.818 | 0.796 | 0.672 | 0.863 | 0.834 | 0.804 | 0.675 | 0.883 |
| f1s1_hsrl_soft | 0.822 | 0.789 | 0.665 | 0.871 | 0.829 | 0.794 | 0.668 | 0.880 |
| f1s2_hsrl | 0.808 | 0.775 | 0.674 | 0.849 | 0.838 | 0.815 | 0.691 | 0.883 |
| f1s2_hsrl_soft | 0.807 | 0.765 | 0.661 | 0.852 | 0.829 | 0.815 | 0.689 | 0.872 |
| f1s3_hsrl | 0.827 | 0.809 | 0.685 | 0.871 | 0.852 | 0.832 | 0.703 | 0.898 |
| f1s3_hsrl_soft | 0.823 | 0.788 | 0.654 | 0.876 | 0.840 | 0.797 | 0.665 | 0.895 |
| f1s4_hsrl | 0.808 | 0.795 | 0.694 | 0.844 | 0.839 | 0.810 | 0.669 | 0.892 |
| f1s4_hsrl_soft | 0.812 | 0.793 | 0.694 | 0.848 | 0.842 | 0.825 | 0.703 | 0.885 |
| f2s0_hsrl | 0.743 | 0.693 | 0.536 | 0.819 | 0.765 | 0.711 | 0.536 | 0.849 |
| f2s0_hsrl_soft | 0.742 | 0.689 | 0.527 | 0.821 | 0.770 | 0.728 | 0.569 | 0.843 |
| f2s1_hsrl | 0.748 | 0.698 | 0.539 | 0.824 | 0.770 | 0.714 | 0.542 | 0.854 |
| f2s1_hsrl_soft | 0.752 | 0.701 | 0.534 | 0.832 | 0.736 | 0.659 | 0.453 | 0.840 |
| f2s2_hsrl | 0.761 | 0.717 | 0.564 | 0.833 | 0.784 | 0.739 | 0.574 | 0.862 |
| f2s2_hsrl_soft | 0.754 | 0.704 | 0.544 | 0.831 | 0.770 | 0.714 | 0.532 | 0.857 |
| f2s3_hsrl | 0.764 | 0.721 | 0.564 | 0.838 | 0.787 | 0.748 | 0.592 | 0.859 |
| f2s3_hsrl_soft | 0.757 | 0.714 | 0.549 | 0.834 | 0.778 | 0.732 | 0.567 | 0.856 |
| f2s4_hsrl | 0.757 | 0.715 | 0.561 | 0.829 | 0.771 | 0.724 | 0.552 | 0.851 |
| f2s4_hsrl_soft | 0.756 | 0.711 | 0.557 | 0.829 | 0.770 | 0.714 | 0.536 | 0.856 |

## 4. Stage III pseudo-labels (vs hidden majority labels)

| config | runs | coverage | precision | prec_unanimous | prec_split | min_coverage |
|---|---|---|---|---|---|---|
| hsrl | 15 | 0.638 ± 0.123 | 0.922 ± 0.010 | 0.965 ± 0.013 | 0.736 ± 0.057 | 0.452 |
| hsrl_soft | 15 | 0.524 ± 0.055 | 0.943 ± 0.017 | 0.981 ± 0.004 | 0.745 ± 0.083 | 0.412 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl | 15 | 30 | 15/15 | 5/15 | 21 22 19 20 27 | 0.036 ± 0.012 | 0.503 ± 0.690 | 0.724 ± 0.042 | 0.79/0.79/0.70 |
| hsrl_soft | 15 | 30 | 15/15 | 5/15 | 21 22 19 20 27 | 0.036 ± 0.012 | 0.503 ± 0.690 | 0.724 ± 0.042 | 0.79/0.79/0.70 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.762 | 0.054 | 14 | 8 | 21.000 | 1.355 | 0.755 |
| f0s0_hsrl_soft | 0.762 | 0.054 | 14 | 8 | 21.000 | 1.355 | 0.755 |
| f0s1_hsrl | 0.684 | 0.049 | 14 | 9 | 22.000 | 1.601 | 0.763 |
| f0s1_hsrl_soft | 0.684 | 0.049 | 14 | 9 | 22.000 | 1.601 | 0.763 |
| f0s2_hsrl | 0.611 | 0.056 | 12 | 10 | 19.000 | 1.519 | 0.815 |
| f0s2_hsrl_soft | 0.611 | 0.056 | 12 | 10 | 19.000 | 1.519 | 0.815 |
| f0s3_hsrl | 0.763 | 0.058 | 13 | 9 | 20.000 | 1.519 | 0.752 |
| f0s3_hsrl_soft | 0.763 | 0.058 | 13 | 9 | 20.000 | 1.519 | 0.752 |
| f0s4_hsrl | 0.810 | 0.041 | 18 | 7 | 27.000 | 1.197 | 0.776 |
| f0s4_hsrl_soft | 0.810 | 0.041 | 18 | 7 | 27.000 | 1.197 | 0.776 |
| f1s0_hsrl | 0.700 | 0.034 | 23 | 8 | nan | 0.069 | 0.721 |
| f1s0_hsrl_soft | 0.700 | 0.034 | 23 | 8 | nan | 0.069 | 0.721 |
| f1s1_hsrl | 0.637 | 0.028 | 25 | 9 | nan | 0.032 | 0.676 |
| f1s1_hsrl_soft | 0.637 | 0.028 | 25 | 9 | nan | 0.032 | 0.676 |
| f1s2_hsrl | 0.563 | 0.022 | 29 | 9 | nan | 0.022 | 0.678 |
| f1s2_hsrl_soft | 0.563 | 0.022 | 29 | 9 | nan | 0.022 | 0.678 |
| f1s3_hsrl | 0.729 | 0.036 | 24 | 8 | nan | 0.048 | 0.706 |
| f1s3_hsrl_soft | 0.729 | 0.036 | 24 | 8 | nan | 0.048 | 0.706 |
| f1s4_hsrl | 0.752 | 0.024 | 28 | 7 | nan | 0.024 | 0.652 |
| f1s4_hsrl_soft | 0.752 | 0.024 | 28 | 7 | nan | 0.024 | 0.652 |
| f2s0_hsrl | 0.743 | 0.024 | 28 | 7 | nan | 0.025 | 0.711 |
| f2s0_hsrl_soft | 0.743 | 0.024 | 28 | 7 | nan | 0.025 | 0.711 |
| f2s1_hsrl | 0.685 | 0.030 | 23 | 8 | nan | 0.041 | 0.723 |
| f2s1_hsrl_soft | 0.685 | 0.030 | 23 | 8 | nan | 0.041 | 0.723 |
| f2s2_hsrl | 0.590 | 0.029 | 26 | 10 | nan | 0.035 | 0.709 |
| f2s2_hsrl_soft | 0.590 | 0.029 | 26 | 10 | nan | 0.035 | 0.709 |
| f2s3_hsrl | 0.780 | 0.033 | 25 | 8 | nan | 0.036 | 0.707 |
| f2s3_hsrl_soft | 0.780 | 0.033 | 25 | 8 | nan | 0.036 | 0.707 |
| f2s4_hsrl | 0.782 | 0.028 | 28 | 7 | nan | 0.029 | 0.719 |
| f2s4_hsrl_soft | 0.782 | 0.028 | 28 | 7 | nan | 0.029 | 0.719 |
