# Aggregate over results/main, results/deviations

Runs: 24; folds [0]; seeds [0, 1, 2]. Test = held-out slides of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III (HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.

## 1. Final test metrics (mean ± std over runs)

| config | runs | acc | bal_acc | macro_f1 | auroc | brier | acc_unanimous | acc_split |
|---|---|---|---|---|---|---|---|---|
| hsrl | 3 | 0.788 ± 0.006 | 0.751 ± 0.007 | 0.761 ± 0.007 | 0.857 ± 0.005 | 0.167 ± 0.004 | 0.861 ± 0.005 | 0.624 ± 0.007 |
| hsrl_no_stage1 | 3 | 0.762 ± 0.006 | 0.711 ± 0.012 | 0.721 ± 0.012 | 0.837 ± 0.003 | 0.173 ± 0.006 | 0.840 ± 0.003 | 0.588 ± 0.012 |
| hsrl_no_t2 | 3 | 0.787 ± 0.006 | 0.763 ± 0.009 | 0.768 ± 0.008 | 0.856 ± 0.004 | 0.171 ± 0.005 | 0.853 ± 0.006 | 0.639 ± 0.005 |
| supervised | 3 | 0.781 ± 0.009 | 0.763 ± 0.014 | 0.765 ± 0.012 | 0.843 ± 0.013 | 0.182 ± 0.009 | 0.842 ± 0.004 | 0.644 ± 0.021 |
| hsrl_boundary | 3 | 0.792 ± 0.018 | 0.758 ± 0.027 | 0.767 ± 0.025 | 0.858 ± 0.015 | 0.164 ± 0.012 | 0.865 ± 0.010 | 0.628 ± 0.039 |
| hsrl_no_t2_s1e60 | 3 | 0.792 ± 0.005 | 0.758 ± 0.008 | 0.767 ± 0.007 | 0.861 ± 0.003 | 0.171 ± 0.004 | 0.866 ± 0.004 | 0.626 ± 0.007 |
| hsrl_s1e60 | 3 | 0.799 ± 0.004 | 0.778 ± 0.011 | 0.782 ± 0.007 | 0.866 ± 0.005 | 0.166 ± 0.002 | 0.864 ± 0.012 | 0.653 ± 0.032 |
| supervised_e65 | 3 | 0.778 ± 0.003 | 0.766 ± 0.005 | 0.765 ± 0.004 | 0.848 ± 0.007 | 0.181 ± 0.003 | 0.836 ± 0.004 | 0.647 ± 0.014 |

### Per fold (mean ± std over seeds)

| config | fold | seeds | acc | bal_acc | auroc | acc_split |
|---|---|---|---|---|---|---|
| hsrl | 0 | 3 | 0.788 ± 0.006 | 0.751 ± 0.007 | 0.857 ± 0.005 | 0.624 ± 0.007 |
| hsrl_no_stage1 | 0 | 3 | 0.762 ± 0.006 | 0.711 ± 0.012 | 0.837 ± 0.003 | 0.588 ± 0.012 |
| hsrl_no_t2 | 0 | 3 | 0.787 ± 0.006 | 0.763 ± 0.009 | 0.856 ± 0.004 | 0.639 ± 0.005 |
| supervised | 0 | 3 | 0.781 ± 0.009 | 0.763 ± 0.014 | 0.843 ± 0.013 | 0.644 ± 0.021 |
| hsrl_boundary | 0 | 3 | 0.792 ± 0.018 | 0.758 ± 0.027 | 0.858 ± 0.015 | 0.628 ± 0.039 |
| hsrl_no_t2_s1e60 | 0 | 3 | 0.792 ± 0.005 | 0.758 ± 0.008 | 0.861 ± 0.003 | 0.626 ± 0.007 |
| hsrl_s1e60 | 0 | 3 | 0.799 ± 0.004 | 0.778 ± 0.011 | 0.866 ± 0.005 | 0.653 ± 0.032 |
| supervised_e65 | 0 | 3 | 0.778 ± 0.003 | 0.766 ± 0.005 | 0.848 ± 0.007 | 0.647 ± 0.014 |

## 2. Paired differences (same fold and seed)

CI = t-interval over all pairs. These pairs are not independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign are the conservative view.

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl_s1e60 − hsrl | overall | acc | 3 | 0.011 | 0.009 | -0.011 | 0.033 | 3/3 | f0:+0.011 | 1 |
| hsrl_s1e60 − hsrl | overall | bal_acc | 3 | 0.027 | 0.018 | -0.017 | 0.071 | 3/3 | f0:+0.027 | 1 |
| hsrl_s1e60 − hsrl | overall | auroc | 3 | 0.008 | 0.009 | -0.014 | 0.031 | 3/3 | f0:+0.008 | 1 |
| hsrl_s1e60 − hsrl | overall | brier | 3 | -0.001 | 0.006 | -0.016 | 0.014 | 1/3 | f0:-0.001 | 1 |
| hsrl_s1e60 − hsrl | split_vote | acc | 3 | 0.029 | 0.038 | -0.065 | 0.124 | 2/3 | f0:+0.029 | 1 |
| hsrl_no_t2_s1e60 − hsrl_no_t2 | overall | acc | 3 | 0.005 | 0.002 | -0.001 | 0.010 | 3/3 | f0:+0.005 | 1 |
| hsrl_no_t2_s1e60 − hsrl_no_t2 | overall | bal_acc | 3 | -0.006 | 0.005 | -0.019 | 0.008 | 0/3 | f0:-0.006 | 1 |
| hsrl_no_t2_s1e60 − hsrl_no_t2 | overall | auroc | 3 | 0.005 | 0.006 | -0.009 | 0.018 | 3/3 | f0:+0.005 | 1 |
| hsrl_no_t2_s1e60 − hsrl_no_t2 | overall | brier | 3 | -0.000 | 0.003 | -0.009 | 0.008 | 1/3 | f0:-0.000 | 1 |
| hsrl_no_t2_s1e60 − hsrl_no_t2 | split_vote | acc | 3 | -0.012 | 0.003 | -0.021 | -0.004 | 0/3 | f0:-0.012 | 1 |
| hsrl_s1e60 − hsrl_no_t2_s1e60 | overall | acc | 3 | 0.007 | 0.003 | -0.000 | 0.014 | 3/3 | f0:+0.007 | 1 |
| hsrl_s1e60 − hsrl_no_t2_s1e60 | overall | bal_acc | 3 | 0.021 | 0.003 | 0.013 | 0.029 | 3/3 | f0:+0.021 | 1 |
| hsrl_s1e60 − hsrl_no_t2_s1e60 | overall | auroc | 3 | 0.005 | 0.005 | -0.008 | 0.018 | 3/3 | f0:+0.005 | 1 |
| hsrl_s1e60 − hsrl_no_t2_s1e60 | overall | brier | 3 | -0.005 | 0.002 | -0.010 | 0.000 | 3/3 | f0:-0.005 | 1 |
| hsrl_s1e60 − hsrl_no_t2_s1e60 | split_vote | acc | 3 | 0.027 | 0.025 | -0.034 | 0.088 | 3/3 | f0:+0.027 | 1 |
| hsrl_boundary − hsrl | overall | acc | 3 | 0.004 | 0.014 | -0.031 | 0.040 | 1/3 | f0:+0.004 | 1 |
| hsrl_boundary − hsrl | overall | bal_acc | 3 | 0.007 | 0.021 | -0.046 | 0.060 | 1/3 | f0:+0.007 | 1 |
| hsrl_boundary − hsrl | overall | auroc | 3 | 0.001 | 0.012 | -0.028 | 0.030 | 1/3 | f0:+0.001 | 1 |
| hsrl_boundary − hsrl | overall | brier | 3 | -0.003 | 0.012 | -0.033 | 0.027 | 2/3 | f0:-0.003 | 1 |
| hsrl_boundary − hsrl | split_vote | acc | 3 | 0.005 | 0.035 | -0.083 | 0.092 | 1/3 | f0:+0.005 | 1 |

## 3. Effect of Stage III (after − before, paired within run)

| comparison | subset | metric | n_pairs | mean_diff | std | ci95_lo | ci95_hi | a_better | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|---|---|
| hsrl[final] − hsrl[before_stage3] | overall | acc | 3 | 0.007 | 0.006 | -0.008 | 0.023 | 3/3 | f0:+0.007 | 1 |
| hsrl[final] − hsrl[before_stage3] | overall | bal_acc | 3 | 0.001 | 0.014 | -0.035 | 0.037 | 1/3 | f0:+0.001 | 1 |
| hsrl[final] − hsrl[before_stage3] | overall | auroc | 3 | 0.006 | 0.006 | -0.009 | 0.021 | 3/3 | f0:+0.006 | 1 |
| hsrl[final] − hsrl[before_stage3] | unanimous | acc | 3 | 0.013 | 0.002 | 0.008 | 0.019 | 3/3 | f0:+0.013 | 1 |
| hsrl[final] − hsrl[before_stage3] | split_vote | acc | 3 | -0.006 | 0.024 | -0.067 | 0.054 | 1/3 | f0:-0.006 | 1 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | acc | 3 | 0.032 | 0.005 | 0.019 | 0.046 | 3/3 | f0:+0.032 | 1 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | bal_acc | 3 | 0.033 | 0.014 | -0.001 | 0.067 | 3/3 | f0:+0.033 | 1 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | overall | auroc | 3 | 0.038 | 0.003 | 0.032 | 0.045 | 3/3 | f0:+0.038 | 1 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | unanimous | acc | 3 | 0.040 | 0.003 | 0.031 | 0.048 | 3/3 | f0:+0.040 | 1 |
| hsrl_no_stage1[final] − hsrl_no_stage1[before_stage3] | split_vote | acc | 3 | 0.015 | 0.010 | -0.010 | 0.040 | 3/3 | f0:+0.015 | 1 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | overall | acc | 3 | 0.009 | 0.010 | -0.017 | 0.035 | 2/3 | f0:+0.009 | 1 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | overall | bal_acc | 3 | 0.007 | 0.017 | -0.035 | 0.049 | 2/3 | f0:+0.007 | 1 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | overall | auroc | 3 | 0.009 | 0.010 | -0.015 | 0.033 | 2/3 | f0:+0.009 | 1 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | unanimous | acc | 3 | 0.011 | 0.003 | 0.005 | 0.018 | 3/3 | f0:+0.011 | 1 |
| hsrl_no_t2[final] − hsrl_no_t2[before_stage3] | split_vote | acc | 3 | 0.003 | 0.029 | -0.068 | 0.074 | 2/3 | f0:+0.003 | 1 |
| hsrl_boundary[final] − hsrl_boundary[before_stage3] | overall | acc | 3 | 0.013 | 0.002 | 0.008 | 0.018 | 3/3 | f0:+0.013 | 1 |
| hsrl_boundary[final] − hsrl_boundary[before_stage3] | overall | bal_acc | 3 | 0.007 | 0.003 | -0.000 | 0.014 | 3/3 | f0:+0.007 | 1 |
| hsrl_boundary[final] − hsrl_boundary[before_stage3] | overall | auroc | 3 | 0.006 | 0.005 | -0.007 | 0.019 | 3/3 | f0:+0.006 | 1 |
| hsrl_boundary[final] − hsrl_boundary[before_stage3] | unanimous | acc | 3 | 0.018 | 0.003 | 0.011 | 0.026 | 3/3 | f0:+0.018 | 1 |
| hsrl_boundary[final] − hsrl_boundary[before_stage3] | split_vote | acc | 3 | 0.000 | 0.001 | -0.001 | 0.002 | 1/3 | f0:+0.000 | 1 |
| hsrl_no_t2_s1e60[final] − hsrl_no_t2_s1e60[before_stage3] | overall | acc | 3 | 0.008 | 0.005 | -0.006 | 0.021 | 3/3 | f0:+0.008 | 1 |
| hsrl_no_t2_s1e60[final] − hsrl_no_t2_s1e60[before_stage3] | overall | bal_acc | 3 | -0.003 | 0.011 | -0.030 | 0.023 | 1/3 | f0:-0.003 | 1 |
| hsrl_no_t2_s1e60[final] − hsrl_no_t2_s1e60[before_stage3] | overall | auroc | 3 | 0.003 | 0.001 | 0.001 | 0.006 | 3/3 | f0:+0.003 | 1 |
| hsrl_no_t2_s1e60[final] − hsrl_no_t2_s1e60[before_stage3] | unanimous | acc | 3 | 0.018 | 0.005 | 0.006 | 0.029 | 3/3 | f0:+0.018 | 1 |
| hsrl_no_t2_s1e60[final] − hsrl_no_t2_s1e60[before_stage3] | split_vote | acc | 3 | -0.014 | 0.014 | -0.048 | 0.019 | 0/3 | f0:-0.014 | 1 |
| hsrl_s1e60[final] − hsrl_s1e60[before_stage3] | overall | acc | 3 | 0.009 | 0.003 | 0.003 | 0.016 | 3/3 | f0:+0.009 | 1 |
| hsrl_s1e60[final] − hsrl_s1e60[before_stage3] | overall | bal_acc | 3 | 0.005 | 0.004 | -0.004 | 0.015 | 3/3 | f0:+0.005 | 1 |
| hsrl_s1e60[final] − hsrl_s1e60[before_stage3] | overall | auroc | 3 | 0.006 | 0.003 | -0.001 | 0.012 | 3/3 | f0:+0.006 | 1 |
| hsrl_s1e60[final] − hsrl_s1e60[before_stage3] | unanimous | acc | 3 | 0.015 | 0.003 | 0.007 | 0.023 | 3/3 | f0:+0.015 | 1 |
| hsrl_s1e60[final] − hsrl_s1e60[before_stage3] | split_vote | acc | 3 | -0.004 | 0.005 | -0.015 | 0.008 | 0/3 | f0:-0.004 | 1 |

### Every run: before (pre) / after (post) Stage III

| run | pre_acc | pre_bal_acc | pre_split_vote_acc | pre_unanimous_acc | post_acc | post_bal_acc | post_split_vote_acc | post_unanimous_acc |
|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.790 | 0.769 | 0.660 | 0.849 | 0.792 | 0.757 | 0.628 | 0.865 |
| f0s0_hsrl_boundary | 0.801 | 0.785 | 0.673 | 0.859 | 0.812 | 0.788 | 0.673 | 0.875 |
| f0s0_hsrl_no_stage1 | 0.732 | 0.683 | 0.578 | 0.800 | 0.767 | 0.721 | 0.598 | 0.843 |
| f0s0_hsrl_no_t2 | 0.785 | 0.766 | 0.662 | 0.840 | 0.782 | 0.753 | 0.633 | 0.849 |
| f0s0_hsrl_no_t2_s1e60 | 0.784 | 0.762 | 0.649 | 0.845 | 0.789 | 0.752 | 0.621 | 0.865 |
| f0s0_hsrl_s1e60 | 0.792 | 0.766 | 0.627 | 0.866 | 0.800 | 0.769 | 0.625 | 0.878 |
| f0s1_hsrl | 0.776 | 0.736 | 0.609 | 0.851 | 0.790 | 0.752 | 0.626 | 0.863 |
| f0s1_hsrl_boundary | 0.773 | 0.736 | 0.603 | 0.850 | 0.785 | 0.745 | 0.604 | 0.866 |
| f0s1_hsrl_no_stage1 | 0.730 | 0.681 | 0.572 | 0.801 | 0.756 | 0.698 | 0.575 | 0.837 |
| f0s1_hsrl_no_t2 | 0.771 | 0.751 | 0.626 | 0.836 | 0.785 | 0.766 | 0.640 | 0.850 |
| f0s1_hsrl_no_t2_s1e60 | 0.784 | 0.764 | 0.638 | 0.850 | 0.788 | 0.754 | 0.624 | 0.862 |
| f0s1_hsrl_s1e60 | 0.786 | 0.773 | 0.656 | 0.845 | 0.794 | 0.776 | 0.647 | 0.861 |
| f0s2_hsrl | 0.774 | 0.746 | 0.621 | 0.843 | 0.781 | 0.743 | 0.616 | 0.855 |
| f0s2_hsrl_boundary | 0.763 | 0.733 | 0.608 | 0.832 | 0.778 | 0.740 | 0.608 | 0.854 |
| f0s2_hsrl_no_stage1 | 0.727 | 0.671 | 0.569 | 0.798 | 0.762 | 0.715 | 0.590 | 0.839 |
| f0s2_hsrl_no_t2 | 0.778 | 0.752 | 0.618 | 0.849 | 0.793 | 0.771 | 0.643 | 0.861 |
| f0s2_hsrl_no_t2_s1e60 | 0.783 | 0.758 | 0.635 | 0.850 | 0.797 | 0.766 | 0.634 | 0.870 |
| f0s2_hsrl_s1e60 | 0.790 | 0.780 | 0.687 | 0.836 | 0.802 | 0.790 | 0.687 | 0.854 |

## 4. Stage III pseudo-labels (vs hidden majority labels)

| config | runs | coverage | precision | prec_unanimous | prec_split | min_coverage |
|---|---|---|---|---|---|---|
| hsrl | 3 | 0.619 ± 0.080 | 0.926 ± 0.010 | 0.958 ± 0.006 | 0.803 ± 0.032 | 0.549 |
| hsrl_no_stage1 | 3 | 0.318 ± 0.008 | 0.934 ± 0.002 | 0.971 ± 0.001 | 0.709 ± 0.013 | 0.312 |
| hsrl_no_t2 | 3 | 0.794 ± 0.004 | 0.899 ± 0.004 | 0.944 ± 0.001 | 0.767 ± 0.020 | 0.790 |
| hsrl_boundary | 3 | 0.605 ± 0.093 | 0.927 ± 0.016 | 0.961 ± 0.008 | 0.795 ± 0.038 | 0.511 |
| hsrl_no_t2_s1e60 | 3 | 0.808 ± 0.010 | 0.904 ± 0.004 | 0.943 ± 0.003 | 0.787 ± 0.009 | 0.799 |
| hsrl_s1e60 | 3 | 0.804 ± 0.010 | 0.902 ± 0.002 | 0.938 ± 0.003 | 0.797 ± 0.011 | 0.795 |

## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)

| config | runs | stage1_epochs | collapsed | escaped | escape_epoch | spread_min | spread_final | knn5_bal_acc_final | t1/t2/t3_active_final |
|---|---|---|---|---|---|---|---|---|---|
| hsrl | 3 | 30 | 3/3 | 0/3 | - | 0.025 ± 0.003 | 0.124 ± 0.152 | 0.845 ± 0.027 | 1.00/1.00/1.00 |
| hsrl_no_t2 | 3 | 30 | 3/3 | 3/3 | 18 18 18 | 0.042 ± 0.002 | 1.476 ± 0.059 | 0.834 ± 0.012 | 0.18/0.63/0.02 |
| hsrl_boundary | 3 | 30 | 3/3 | 1/3 | 27 | 0.063 ± 0.004 | 0.616 ± 0.798 | 0.818 ± 0.036 | 0.91/0.77/0.76 |
| hsrl_no_t2_s1e60 | 3 | 60 | 3/3 | 3/3 | 18 18 18 | 0.042 ± 0.002 | 1.652 ± 0.027 | 0.850 ± 0.009 | 0.03/0.79/0.01 |
| hsrl_s1e60 | 3 | 60 | 3/3 | 3/3 | 30 34 32 | 0.025 ± 0.003 | 1.360 ± 0.145 | 0.861 ± 0.007 | 0.07/0.60/0.02 |

Per run:

| run | spread_init | spread_min | epoch_min | collapse_epoch | escape_epoch | spread_final | knn5_bal_acc_final |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl | 0.761 | 0.028 | 21 | 6 | nan | 0.300 | 0.873 |
| f0s0_hsrl_no_t2 | 0.761 | 0.045 | 12 | 5 | 18.000 | 1.544 | 0.848 |
| f0s1_hsrl | 0.699 | 0.023 | 24 | 6 | nan | 0.029 | 0.819 |
| f0s1_hsrl_no_t2 | 0.699 | 0.042 | 12 | 6 | 18.000 | 1.436 | 0.830 |
| f0s2_hsrl | 0.608 | 0.024 | 22 | 7 | nan | 0.043 | 0.842 |
| f0s2_hsrl_no_t2 | 0.608 | 0.040 | 13 | 6 | 18.000 | 1.449 | 0.824 |
| f0s0_hsrl_boundary | 0.761 | 0.066 | 19 | 14 | 27.000 | 1.534 | 0.859 |
| f0s0_hsrl_no_t2_s1e60 | 0.761 | 0.045 | 12 | 5 | 18.000 | 1.664 | 0.856 |
| f0s0_hsrl_s1e60 | 0.761 | 0.028 | 21 | 6 | 30.000 | 1.250 | 0.853 |
| f0s1_hsrl_boundary | 0.699 | 0.065 | 20 | 17 | nan | 0.225 | 0.807 |
| f0s1_hsrl_no_t2_s1e60 | 0.699 | 0.042 | 12 | 6 | 18.000 | 1.671 | 0.840 |
| f0s1_hsrl_s1e60 | 0.699 | 0.023 | 24 | 6 | 34.000 | 1.305 | 0.863 |
| f0s2_hsrl_boundary | 0.608 | 0.059 | 22 | 16 | nan | 0.089 | 0.789 |
| f0s2_hsrl_no_t2_s1e60 | 0.608 | 0.040 | 13 | 6 | 18.000 | 1.621 | 0.855 |
| f0s2_hsrl_s1e60 | 0.608 | 0.024 | 22 | 7 | 32.000 | 1.525 | 0.867 |
