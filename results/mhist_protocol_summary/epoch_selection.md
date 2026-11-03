# Epoch selection on MHIST (diagnostic, D41)

Test metrics in % (mean ± std over draws). final = end of training; best_val = epoch with the highest validation accuracy; best_test = epoch with the highest TEST accuracy (invalid selection, shown only to measure the possible inflation); inflation = best_test − final.

| config | runs | final_acc | best_val_acc | best_test_acc | inflation_acc | final_macro_f1 | best_val_macro_f1 | best_test_macro_f1 | inflation_macro_f1 |
|---|---|---|---|---|---|---|---|---|---|
| hsrl_epochlog | 5 | 77.564 ± 2.239 | 76.806 ± 2.501 | 78.076 ± 1.826 | 0.512 ± 0.595 | 75.436 ± 2.510 | 74.558 ± 2.621 | 75.976 ± 2.294 | 0.540 ± 0.594 |
| supervised_epochlog | 5 | 76.746 ± 2.751 | 77.236 ± 2.451 | 78.322 ± 1.639 | 1.576 ± 1.392 | 74.854 ± 2.739 | 75.286 ± 3.054 | 76.670 ± 2.124 | 1.816 ± 0.988 |

## Per run

| run | fold | seed | cfg | n_epochs | best_test_epoch | best_val_epoch | final_acc | best_val_acc | best_test_acc | inflation_acc | final_macro_f1 | best_val_macro_f1 | best_test_macro_f1 | inflation_macro_f1 | final_bal_acc | best_val_bal_acc | best_test_bal_acc | inflation_bal_acc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl_epochlog | 0 | 0 | hsrl_epochlog | 15 | stage3:5 | stage2:0 | 0.784 | 0.752 | 0.787 | 0.003 | 0.776 | 0.733 | 0.777 | 0.001 | 0.790 | 0.733 | 0.786 | -0.004 |
| f0s0_supervised_epochlog | 0 | 0 | supervised_epochlog | 35 | supervised:33 | supervised:28 | 0.787 | 0.783 | 0.789 | 0.002 | 0.776 | 0.772 | 0.777 | 0.002 | 0.782 | 0.780 | 0.782 | 0.001 |
| f1s1_hsrl_epochlog | 1 | 1 | hsrl_epochlog | 15 | stage3:7 | stage3:7 | 0.802 | 0.807 | 0.807 | 0.004 | 0.783 | 0.790 | 0.790 | 0.007 | 0.777 | 0.787 | 0.787 | 0.010 |
| f1s1_supervised_epochlog | 1 | 1 | supervised_epochlog | 35 | supervised:31 | supervised:22 | 0.785 | 0.802 | 0.802 | 0.017 | 0.768 | 0.789 | 0.790 | 0.021 | 0.768 | 0.790 | 0.793 | 0.025 |
| f2s2_hsrl_epochlog | 2 | 2 | hsrl_epochlog | 15 | stage3:4 | stage3:3 | 0.773 | 0.767 | 0.776 | 0.003 | 0.749 | 0.745 | 0.753 | 0.004 | 0.743 | 0.742 | 0.747 | 0.005 |
| f2s2_supervised_epochlog | 2 | 2 | supervised_epochlog | 35 | supervised:18 | supervised:23 | 0.766 | 0.775 | 0.784 | 0.018 | 0.750 | 0.759 | 0.771 | 0.021 | 0.751 | 0.760 | 0.775 | 0.024 |
| f3s3_hsrl_epochlog | 3 | 3 | hsrl_epochlog | 15 | stage3:6 | stage3:9 | 0.741 | 0.741 | 0.756 | 0.015 | 0.722 | 0.722 | 0.737 | 0.015 | 0.722 | 0.722 | 0.735 | 0.013 |
| f3s3_supervised_epochlog | 3 | 3 | supervised_epochlog | 35 | supervised:26 | supervised:20 | 0.721 | 0.736 | 0.757 | 0.037 | 0.706 | 0.714 | 0.733 | 0.028 | 0.711 | 0.712 | 0.729 | 0.018 |
| f4s4_hsrl_epochlog | 4 | 4 | hsrl_epochlog | 15 | stage3:9 | stage3:8 | 0.778 | 0.774 | 0.778 | 0.000 | 0.742 | 0.737 | 0.742 | 0.000 | 0.730 | 0.726 | 0.730 | 0.000 |
| f4s4_supervised_epochlog | 4 | 4 | supervised_epochlog | 35 | supervised:18 | supervised:26 | 0.779 | 0.766 | 0.783 | 0.004 | 0.744 | 0.730 | 0.762 | 0.019 | 0.732 | 0.720 | 0.758 | 0.026 |
