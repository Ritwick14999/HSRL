# D46 / D47 follow-up check

Pre-registered in ASSUMPTIONS.md (D46, D47). Balanced accuracy in points, paired. CI = t-interval over draws (all draws share one test set, so it covers labelled-set and training variation only).

## MHIST: balanced accuracy per draw (%)

| draw | hsrl | hsrl_soft | supervised | supervised_soft | hsrl_soft_rerun | supported | supported_random | supported_conf | interval | worstcase | joint | supported_gap | supported_gap_shuffled | supported_similarity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 | 79.0 | 79.2 | 78.2 | 77.0 | 77.9 | 79.0 | 78.9 | 80.5 | 79.1 | 79.5 | 77.8 | 78.9 | 80.0 | 79.3 |
| 1.0 | 77.7 | 80.2 | 76.8 | 79.1 | 80.5 | 80.4 | 79.0 | 79.6 | 78.8 | 78.8 | 79.0 | 80.2 | 80.6 | 80.6 |
| 2.0 | 74.3 | 75.7 | 75.1 | 79.0 | 76.1 | 77.7 | 76.9 | 78.6 | 78.6 | 77.3 | 78.6 | 78.6 | 76.7 | 77.5 |
| 3.0 | 72.2 | 73.1 | 71.0 | 73.8 | 74.0 | 74.8 | 73.2 | 77.4 | 76.3 | 74.3 | 73.6 | 77.8 | 76.3 | 76.0 |
| 4.0 | 73.0 | 77.5 | 73.2 | 73.7 | 76.9 | 76.2 | 76.8 | 77.3 | 77.2 | 77.7 | 77.5 | 76.4 | 76.8 | 77.9 |
| 5.0 | 78.5 | 78.8 | 76.2 | 77.4 | 80.7 | 79.0 | 78.2 | 78.3 | 79.7 | 81.1 | 80.2 | 77.9 | 77.1 | 80.0 |
| 6.0 | 75.1 | 77.6 | 74.8 | 74.3 | 77.8 | 78.8 | 75.0 | 77.2 | 76.2 | 76.5 | 78.8 | 77.4 | 77.1 | 76.7 |
| 7.0 | 77.5 | 78.4 | 74.8 | 76.8 | 74.4 | 77.5 | 78.5 | 78.0 | 80.6 | 78.1 | 78.7 | 79.5 | 77.8 | 78.8 |
| 8.0 | 70.5 | 74.2 | 72.4 | 75.4 | 76.0 | 78.1 | 75.9 | 76.0 | 75.3 | 76.8 | 78.6 | 77.1 | 77.8 | 76.5 |
| 9.0 | 69.4 | 73.2 | 77.6 | 75.5 | 76.0 | 76.6 | 75.7 | 73.6 | 77.7 | 76.6 | 73.8 | 77.0 | 75.2 | 76.9 |

## D45 / D47 comparisons (Δ balanced accuracy, points; pass = mean ≥ +1.0 and positive in the required draws)

| comparison | view | mean | up | ci95 | pass |
|---|---|---|---|---|---|
| supported − hsrl_soft | draws 0-4 (5-draw verdict, rule 4/5) | 0.480 | 3/5 | [-1.21, +2.16] | no |
| supported − hsrl_soft | draws 5-9 (replication, rule 4/5) | 1.570 | 4/5 | [-0.99, +4.12] | PASS |
| supported − hsrl_soft | draws 0-9 (primary, rule 8/10) | 1.020 | 7/10 | [-0.23, +2.27] | no |
| supported_random − hsrl_soft | draws 0-4 (5-draw verdict, rule 4/5) | -0.180 | 2/5 | [-1.27, +0.91] | no |
| supported_random − hsrl_soft | draws 5-9 (replication, rule 4/5) | 0.190 | 3/5 | [-2.32, +2.71] | no |
| supported_random − hsrl_soft | draws 0-9 (primary, rule 8/10) | 0.010 | 5/10 | [-1.06, +1.07] | no |
| supported_conf − hsrl_soft | draws 0-4 (5-draw verdict, rule 4/5) | 1.530 | 3/5 | [-1.04, +4.10] | no |
| supported_conf − hsrl_soft | draws 5-9 (replication, rule 4/5) | 0.200 | 2/5 | [-1.06, +1.46] | no |
| supported_conf − hsrl_soft | draws 0-9 (primary, rule 8/10) | 0.870 | 5/10 | [-0.34, +2.08] | no |
| interval − hsrl_soft | draws 0-4 (5-draw verdict, rule 4/5) | 0.860 | 2/5 | [-1.69, +3.41] | no |
| interval − hsrl_soft | draws 5-9 (replication, rule 4/5) | 1.460 | 4/5 | [-1.18, +4.10] | PASS |
| interval − hsrl_soft | draws 0-9 (primary, rule 8/10) | 1.160 | 6/10 | [-0.27, +2.59] | no |
| worstcase − hsrl_soft | draws 0-4 (5-draw verdict, rule 4/5) | 0.370 | 4/5 | [-1.09, +1.84] | no |
| worstcase − hsrl_soft | draws 5-9 (replication, rule 4/5) | 1.370 | 3/5 | [-1.07, +3.81] | no |
| worstcase − hsrl_soft | draws 0-9 (primary, rule 8/10) | 0.870 | 7/10 | [-0.28, +2.03] | no |
| joint − hsrl_soft | draws 0-4 (5-draw verdict, rule 4/5) | 0.150 | 3/5 | [-1.99, +2.29] | no |
| joint − hsrl_soft | draws 5-9 (replication, rule 4/5) | 1.550 | 5/5 | [-0.52, +3.61] | PASS |
| joint − hsrl_soft | draws 0-9 (primary, rule 8/10) | 0.850 | 8/10 | [-0.41, +2.10] | no |
| supported_gap − hsrl_soft | draws 0-4 (5-draw verdict, rule 4/5) | 1.230 | 2/5 | [-1.81, +4.27] | no |
| supported_gap − hsrl_soft | draws 5-9 (replication, rule 4/5) | 1.360 | 3/5 | [-1.12, +3.85] | no |
| supported_gap − hsrl_soft | draws 0-9 (primary, rule 8/10) | 1.300 | 5/10 | [-0.21, +2.80] | no |
| supported_gap_shuffled − hsrl_soft | draws 0-4 (5-draw verdict, rule 4/5) | 0.920 | 4/5 | [-0.88, +2.71] | no |
| supported_gap_shuffled − hsrl_soft | draws 5-9 (replication, rule 4/5) | 0.560 | 2/5 | [-2.14, +3.25] | no |
| supported_gap_shuffled − hsrl_soft | draws 0-9 (primary, rule 8/10) | 0.740 | 6/10 | [-0.52, +1.99] | no |
| supported_similarity − hsrl_soft | draws 0-4 (5-draw verdict, rule 4/5) | 1.130 | 5/5 | [-0.35, +2.61] | PASS |
| supported_similarity − hsrl_soft | draws 5-9 (replication, rule 4/5) | 1.330 | 4/5 | [-0.85, +3.52] | PASS |
| supported_similarity − hsrl_soft | draws 0-9 (primary, rule 8/10) | 1.230 | 9/10 | [+0.21, +2.25] | PASS |
| supported − supported_random | draws 0-4 (5-draw verdict, rule 4/5) | 0.660 | 4/5 | [-0.44, +1.75] | no |
| supported − supported_random | draws 5-9 (replication, rule 4/5) | 1.370 | 4/5 | [-0.86, +3.60] | PASS |
| supported − supported_random | draws 0-9 (primary, rule 8/10) | 1.010 | 8/10 | [+0.02, +2.01] | PASS |
| supported − supported_conf | draws 0-4 (5-draw verdict, rule 4/5) | -1.060 | 1/5 | [-2.58, +0.47] | no |
| supported − supported_conf | draws 5-9 (replication, rule 4/5) | 1.370 | 4/5 | [-0.31, +3.04] | PASS |
| supported − supported_conf | draws 0-9 (primary, rule 8/10) | 0.150 | 5/10 | [-1.10, +1.41] | no |
| joint − worstcase | draws 0-4 (5-draw verdict, rule 4/5) | -0.230 | 2/5 | [-1.61, +1.15] | no |
| joint − worstcase | draws 5-9 (replication, rule 4/5) | 0.180 | 3/5 | [-2.45, +2.80] | no |
| joint − worstcase | draws 0-9 (primary, rule 8/10) | -0.020 | 5/10 | [-1.17, +1.13] | no |
| supported_gap − supported | draws 0-4 (5-draw verdict, rule 4/5) | 0.750 | 3/5 | [-0.92, +2.42] | no |
| supported_gap − supported | draws 5-9 (replication, rule 4/5) | -0.200 | 2/5 | [-1.94, +1.54] | no |
| supported_gap − supported | draws 0-9 (primary, rule 8/10) | 0.280 | 5/10 | [-0.72, +1.27] | no |
| supported_gap − supported_gap_shuffled | draws 0-4 (5-draw verdict, rule 4/5) | 0.310 | 2/5 | [-1.29, +1.91] | no |
| supported_gap − supported_gap_shuffled | draws 5-9 (replication, rule 4/5) | 0.810 | 4/5 | [-0.48, +2.10] | no |
| supported_gap − supported_gap_shuffled | draws 0-9 (primary, rule 8/10) | 0.560 | 6/10 | [-0.25, +1.37] | no |
| supported_similarity − supported | draws 0-4 (5-draw verdict, rule 4/5) | 0.650 | 4/5 | [-0.36, +1.67] | no |
| supported_similarity − supported | draws 5-9 (replication, rule 4/5) | -0.230 | 3/5 | [-2.16, +1.69] | no |
| supported_similarity − supported | draws 0-9 (primary, rule 8/10) | 0.210 | 7/10 | [-0.69, +1.11] | no |

## Secondary (D46.4) and rerun noise

| comparison | view | mean | up | ci95 | pass |
|---|---|---|---|---|---|
| hsrl − supervised | draws 0-9 (primary, rule 8/10) | -0.280 | 6/10 | [-2.49, +1.93] | no |
| hsrl_soft − supervised_soft | draws 0-9 (primary, rule 8/10) | 0.600 | 6/10 | [-1.08, +2.29] | no |
| hsrl_soft_rerun − hsrl_soft | draws 0-9 (primary, rule 8/10) | 0.230 | 7/10 | [-1.15, +1.61] | no |

## D46.3: weak-draw pattern vs an HSRL rerun

| draws | six losses − hsrl_soft | rerun − hsrl_soft | six losses − rerun |
|---|---|---|---|
| weak draws 2, 3, 4, 8, 9 | 1.750 | 1.070 | 0.680 |
| other draws | -0.160 | -0.610 | 0.450 |

Per loss, weak draws, loss − rerun: {'supported': np.float64(0.88), 'supported_random': np.float64(-0.11), 'supported_conf': np.float64(0.79), 'interval': np.float64(1.21), 'worstcase': np.float64(0.73), 'joint': np.float64(0.59)}

**Reading:** six losses − rerun on the weak draws = +0.68 points (bar +1.0): the weak-draw gain is attributed to rerun noise (regression to the mean).

## Gleason, linked votes: gap margin (D47.3)

| fold | seed | hsrl_soft | supported_linked | supported_gap_linked |
|---|---|---|---|---|
| 0.0 | 0.0 | 76.4 | 76.9 | 74.9 |
| 0.0 | 1.0 | 74.1 | 78.1 | 76.0 |
| 1.0 | 0.0 | 77.9 | 81.5 | 80.5 |
| 1.0 | 1.0 | 78.8 | 80.7 | 82.8 |
| 2.0 | 0.0 | 76.9 | 78.4 | 75.2 |
| 2.0 | 1.0 | 72.6 | 75.1 | 73.9 |

- supported_gap_linked − supported_linked: mean -1.24, positive 1/6, fold means -2.06 / +0.55 / -2.20 → no (pre-registered test)
- supported_gap_linked − hsrl_soft: mean +1.08, positive 4/6, fold means +0.17 / +3.29 / -0.22 → no (reported alongside)
