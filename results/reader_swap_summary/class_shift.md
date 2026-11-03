# Soft vs hard targets: class shift within each label-set setting

Test non-tie patches. Paired differences soft − hard on the same (fold, seed); CI = t-interval over pairs (optimistic, 3 test-slide sets). Compare differences across settings, never raw values (different label sets).

## Setting: with Map1 (label set `labels_benign-drop`)

| fold | kept patches | labelled (used) | unlabelled pool | val | test | labelled G3: mean q | labelled G3: share with any G4/5 vote | labelled G4/5: mean 1−q | labelled G4/5: share with any G3 vote | mean readers per labelled patch |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 8897 | 488 | 4548 | 840 | 3004 | 0.122 | 0.43 | 0.05 | 0.18 | 4.1 |
| 1 | 8897 | 470 | 4409 | 811 | 3186 | 0.152 | 0.56 | 0.065 | 0.22 | 4.1 |
| 2 | 8897 | 509 | 4781 | 878 | 2707 | 0.142 | 0.49 | 0.044 | 0.15 | 3.93 |

### Supervised (35 ep), final

| target | runs | pred_g4_rate | recall_g3 | recall_g4 | bal_acc | brier | acc_split | acc_unanimous |
|---|---|---|---|---|---|---|---|---|
| hard | 15 | 0.621 ± 0.040 | 0.730 ± 0.066 | 0.832 ± 0.032 | 0.781 ± 0.026 | 0.171 ± 0.019 | 0.662 ± 0.028 | 0.846 ± 0.020 |
| soft | 15 | 0.643 ± 0.036 | 0.709 ± 0.059 | 0.854 ± 0.031 | 0.781 ± 0.026 | 0.142 ± 0.015 | 0.655 ± 0.028 | 0.857 ± 0.021 |
| Δ soft − hard | 15 | +0.022 [+0.007, +0.037] | -0.021 [-0.043, +0.000] | +0.023 [+0.011, +0.034] | +0.001 [-0.006, +0.007] | -0.029 [-0.032, -0.026] | -0.007 [-0.017, +0.002] | +0.011 [+0.008, +0.015] |

### HSRL (Stage I 30 ep), after Stage II

| target | runs | pred_g4_rate | recall_g3 | recall_g4 | bal_acc | brier | acc_split | acc_unanimous |
|---|---|---|---|---|---|---|---|---|
| hard | 15 | 0.632 ± 0.052 | 0.690 ± 0.068 | 0.826 ± 0.041 | 0.758 ± 0.017 | 0.163 ± 0.010 | 0.644 ± 0.022 | 0.828 ± 0.017 |
| soft | 15 | 0.682 ± 0.035 | 0.625 ± 0.051 | 0.866 ± 0.027 | 0.745 ± 0.015 | 0.153 ± 0.007 | 0.621 ± 0.023 | 0.837 ± 0.014 |
| Δ soft − hard | 15 | +0.049 [+0.033, +0.065] | -0.065 [-0.085, -0.045] | +0.040 [+0.026, +0.054] | -0.013 [-0.016, -0.009] | -0.010 [-0.017, -0.004] | -0.023 [-0.033, -0.013] | +0.009 [+0.004, +0.014] |

### HSRL (Stage I 30 ep), final (after Stage III)

| target | runs | pred_g4_rate | recall_g3 | recall_g4 | bal_acc | brier | acc_split | acc_unanimous |
|---|---|---|---|---|---|---|---|---|
| hard | 15 | 0.656 ± 0.054 | 0.686 ± 0.076 | 0.861 ± 0.041 | 0.773 ± 0.022 | 0.160 ± 0.019 | 0.652 ± 0.026 | 0.853 ± 0.014 |
| soft | 15 | 0.695 ± 0.043 | 0.632 ± 0.071 | 0.892 ± 0.029 | 0.762 ± 0.024 | 0.158 ± 0.018 | 0.635 ± 0.034 | 0.858 ± 0.010 |
| Δ soft − hard | 15 | +0.039 [+0.020, +0.058] | -0.053 [-0.080, -0.026] | +0.031 [+0.016, +0.046] | -0.011 [-0.019, -0.003] | -0.002 [-0.005, +0.002] | -0.017 [-0.031, -0.003] | +0.005 [-0.000, +0.011] |

## Setting: Map1 excluded (label set `labels_benign-drop_excl-r1`)

| fold | kept patches | labelled (used) | unlabelled pool | val | test | labelled G3: mean q | labelled G3: share with any G4/5 vote | labelled G4/5: mean 1−q | labelled G4/5: share with any G3 vote | mean readers per labelled patch |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 7212 | 415 | 3786 | 700 | 2305 | 0.077 | 0.25 | 0.034 | 0.11 | 3.39 |
| 1 | 7212 | 386 | 3511 | 647 | 2664 | 0.081 | 0.26 | 0.058 | 0.19 | 3.39 |
| 2 | 7212 | 420 | 3834 | 709 | 2243 | 0.074 | 0.24 | 0.052 | 0.16 | 3.32 |

### Supervised (35 ep), final

| target | runs | pred_g4_rate | recall_g3 | recall_g4 | bal_acc | brier | acc_split | acc_unanimous |
|---|---|---|---|---|---|---|---|---|
| hard | 15 | 0.646 ± 0.057 | 0.682 ± 0.083 | 0.842 ± 0.058 | 0.762 ± 0.025 | 0.179 ± 0.024 | 0.598 ± 0.048 | 0.819 ± 0.023 |
| soft | 15 | 0.639 ± 0.054 | 0.707 ± 0.098 | 0.846 ± 0.046 | 0.776 ± 0.031 | 0.152 ± 0.018 | 0.596 ± 0.054 | 0.833 ± 0.016 |
| Δ soft − hard | 15 | -0.006 [-0.024, +0.012] | +0.025 [+0.004, +0.046] | +0.005 [-0.015, +0.024] | +0.015 [+0.006, +0.023] | -0.027 [-0.034, -0.020] | -0.002 [-0.012, +0.008] | +0.015 [+0.004, +0.025] |

### HSRL (Stage I 30 ep), after Stage II

| target | runs | pred_g4_rate | recall_g3 | recall_g4 | bal_acc | brier | acc_split | acc_unanimous |
|---|---|---|---|---|---|---|---|---|
| hard | 15 | 0.671 ± 0.039 | 0.630 ± 0.061 | 0.853 ± 0.031 | 0.742 ± 0.018 | 0.169 ± 0.013 | 0.614 ± 0.049 | 0.803 ± 0.016 |
| soft | 15 | 0.671 ± 0.047 | 0.631 ± 0.073 | 0.852 ± 0.042 | 0.742 ± 0.019 | 0.163 ± 0.009 | 0.611 ± 0.051 | 0.802 ± 0.016 |
| Δ soft − hard | 15 | -0.001 [-0.016, +0.015] | +0.001 [-0.020, +0.022] | -0.001 [-0.013, +0.011] | -0.000 [-0.006, +0.005] | -0.005 [-0.008, -0.002] | -0.003 [-0.010, +0.005] | -0.001 [-0.004, +0.002] |

### HSRL (Stage I 30 ep), final (after Stage III)

| target | runs | pred_g4_rate | recall_g3 | recall_g4 | bal_acc | brier | acc_split | acc_unanimous |
|---|---|---|---|---|---|---|---|---|
| hard | 15 | 0.683 ± 0.038 | 0.651 ± 0.075 | 0.883 ± 0.028 | 0.767 ± 0.025 | 0.160 ± 0.024 | 0.623 ± 0.058 | 0.832 ± 0.010 |
| soft | 15 | 0.675 ± 0.055 | 0.656 ± 0.097 | 0.873 ± 0.045 | 0.764 ± 0.027 | 0.162 ± 0.023 | 0.620 ± 0.057 | 0.826 ± 0.007 |
| Δ soft − hard | 15 | -0.008 [-0.026, +0.010] | +0.005 [-0.018, +0.027] | -0.010 [-0.026, +0.006] | -0.003 [-0.007, +0.002] | +0.002 [-0.001, +0.005] | -0.003 [-0.009, +0.003] | -0.006 [-0.011, -0.001] |

## Setting: Map4 excluded (label set `labels_benign-drop_excl-r4`)

| fold | kept patches | labelled (used) | unlabelled pool | val | test | labelled G3: mean q | labelled G3: share with any G4/5 vote | labelled G4/5: mean 1−q | labelled G4/5: share with any G3 vote | mean readers per labelled patch |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 7471 | 425 | 3870 | 708 | 2463 | 0.14 | 0.45 | 0.044 | 0.14 | 3.42 |
| 1 | 7471 | 400 | 3656 | 674 | 2735 | 0.142 | 0.46 | 0.061 | 0.19 | 3.36 |
| 2 | 7471 | 441 | 4013 | 739 | 2273 | 0.135 | 0.44 | 0.063 | 0.19 | 3.28 |

### Supervised (35 ep), final

| target | runs | pred_g4_rate | recall_g3 | recall_g4 | bal_acc | brier | acc_split | acc_unanimous |
|---|---|---|---|---|---|---|---|---|
| hard | 15 | 0.671 ± 0.032 | 0.671 ± 0.077 | 0.872 ± 0.025 | 0.772 ± 0.038 | 0.167 ± 0.029 | 0.624 ± 0.041 | 0.863 ± 0.021 |
| soft | 15 | 0.691 ± 0.028 | 0.659 ± 0.080 | 0.896 ± 0.014 | 0.778 ± 0.039 | 0.139 ± 0.023 | 0.630 ± 0.047 | 0.876 ± 0.018 |
| Δ soft − hard | 15 | +0.020 [+0.005, +0.035] | -0.012 [-0.036, +0.011] | +0.025 [+0.011, +0.038] | +0.006 [-0.003, +0.015] | -0.028 [-0.034, -0.022] | +0.005 [-0.012, +0.022] | +0.013 [+0.007, +0.019] |

### HSRL (Stage I 30 ep), after Stage II

| target | runs | pred_g4_rate | recall_g3 | recall_g4 | bal_acc | brier | acc_split | acc_unanimous |
|---|---|---|---|---|---|---|---|---|
| hard | 15 | 0.692 ± 0.035 | 0.619 ± 0.089 | 0.874 ± 0.015 | 0.747 ± 0.041 | 0.160 ± 0.027 | 0.604 ± 0.060 | 0.847 ± 0.017 |
| soft | 15 | 0.721 ± 0.028 | 0.579 ± 0.078 | 0.896 ± 0.015 | 0.738 ± 0.038 | 0.153 ± 0.019 | 0.592 ± 0.059 | 0.850 ± 0.018 |
| Δ soft − hard | 15 | +0.029 [+0.019, +0.038] | -0.040 [-0.053, -0.027] | +0.022 [+0.015, +0.029] | -0.009 [-0.013, -0.005] | -0.007 [-0.013, -0.001] | -0.012 [-0.016, -0.008] | +0.003 [+0.001, +0.006] |

### HSRL (Stage I 30 ep), final (after Stage III)

| target | runs | pred_g4_rate | recall_g3 | recall_g4 | bal_acc | brier | acc_split | acc_unanimous |
|---|---|---|---|---|---|---|---|---|
| hard | 15 | 0.715 ± 0.033 | 0.614 ± 0.090 | 0.907 ± 0.015 | 0.760 ± 0.043 | 0.159 ± 0.032 | 0.611 ± 0.059 | 0.870 ± 0.018 |
| soft | 15 | 0.724 ± 0.048 | 0.594 ± 0.108 | 0.911 ± 0.026 | 0.753 ± 0.047 | 0.161 ± 0.031 | 0.601 ± 0.072 | 0.867 ± 0.018 |
| Δ soft − hard | 15 | +0.010 [-0.011, +0.030] | -0.019 [-0.054, +0.016] | +0.004 [-0.008, +0.017] | -0.008 [-0.020, +0.005] | +0.002 [-0.004, +0.008] | -0.009 [-0.029, +0.011] | -0.003 [-0.006, +0.001] |

## Side by side: soft − hard shift in each setting (within-setting paired differences)

| comparison | metric | with Map1 | Map1 excluded | Map4 excluded |
|---|---|---|---|---|
| Supervised (35 ep), final | pred_g4_rate | 0.022 | -0.006 | 0.020 |
| Supervised (35 ep), final | recall_g3 | -0.021 | 0.025 | -0.012 |
| Supervised (35 ep), final | recall_g4 | 0.023 | 0.005 | 0.025 |
| Supervised (35 ep), final | bal_acc | 0.001 | 0.015 | 0.006 |
| Supervised (35 ep), final | brier | -0.029 | -0.027 | -0.028 |
| Supervised (35 ep), final | acc_split | -0.007 | -0.002 | 0.005 |
| Supervised (35 ep), final | acc_unanimous | 0.011 | 0.015 | 0.013 |
| HSRL (Stage I 30 ep), after Stage II | pred_g4_rate | 0.049 | -0.001 | 0.029 |
| HSRL (Stage I 30 ep), after Stage II | recall_g3 | -0.065 | 0.001 | -0.040 |
| HSRL (Stage I 30 ep), after Stage II | recall_g4 | 0.040 | -0.001 | 0.022 |
| HSRL (Stage I 30 ep), after Stage II | bal_acc | -0.013 | -0.000 | -0.009 |
| HSRL (Stage I 30 ep), after Stage II | brier | -0.010 | -0.005 | -0.007 |
| HSRL (Stage I 30 ep), after Stage II | acc_split | -0.023 | -0.003 | -0.012 |
| HSRL (Stage I 30 ep), after Stage II | acc_unanimous | 0.009 | -0.001 | 0.003 |
| HSRL (Stage I 30 ep), final (after Stage III) | pred_g4_rate | 0.039 | -0.008 | 0.010 |
| HSRL (Stage I 30 ep), final (after Stage III) | recall_g3 | -0.053 | 0.005 | -0.019 |
| HSRL (Stage I 30 ep), final (after Stage III) | recall_g4 | 0.031 | -0.010 | 0.004 |
| HSRL (Stage I 30 ep), final (after Stage III) | bal_acc | -0.011 | -0.003 | -0.008 |
| HSRL (Stage I 30 ep), final (after Stage III) | brier | -0.002 | 0.002 | 0.002 |
| HSRL (Stage I 30 ep), final (after Stage III) | acc_split | -0.017 | -0.003 | -0.009 |
| HSRL (Stage I 30 ep), final (after Stage III) | acc_unanimous | 0.005 | -0.006 | -0.003 |

Full rows with CIs, per-fold means and sign counts: `class_shift_paired.csv`.
