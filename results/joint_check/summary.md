# Step 1: does the joint four-image loss differ from the independent pairwise worst case?

No training. End-of-Stage-I embeddings of each HSRL run; votes of labelled training images only. gap > 1e-06 counts as a difference. 'vertices' = the 2^m pairwise worst cases (m = pairs with L < U); 'all vertices feasible' means joint = independent for every possible embedding. Mean ± std over runs.

## Per dataset, tuple set and allocation model

| dataset | set | model | runs | tuples/run | pct_gap | mean_rel_gap_given_gap | p90_rel_gap | mean_grad_cos_given_gap | pct_all_vertices_feasible | mean_frac_vertices_feasible |
|---|---|---|---|---|---|---|---|---|---|---|
| gleason | mined_last_epoch | relax | 15 | 501 | 11.089 ± 8.184 | 0.086 ± 0.034 | 0.052 ± 0.049 | 0.966 ± 0.007 | 86.067 ± 5.980 | 0.941 ± 0.027 |
| gleason | random | relax | 15 | 1000 | 7.693 ± 5.637 | 0.086 ± 0.031 | 0.031 ± 0.044 | 0.965 ± 0.015 | 89.500 ± 4.405 | 0.958 ± 0.019 |
| mhist | mined_last_epoch | exact | 5 | 224 | 21.875 ± 7.182 | 0.081 ± 0.019 | 0.079 ± 0.035 | 0.920 ± 0.021 | 36.500 ± 12.365 | 0.684 ± 0.087 |
| mhist | mined_last_epoch | relax | 5 | 224 | 21.875 ± 7.182 | 0.081 ± 0.019 | 0.079 ± 0.035 | 0.920 ± 0.021 | 36.500 ± 12.365 | 0.684 ± 0.087 |
| mhist | random | exact | 5 | 1000 | 13.020 ± 3.730 | 0.080 ± 0.018 | 0.027 ± 0.025 | 0.932 ± 0.011 | 42.800 ± 2.159 | 0.751 ± 0.014 |
| mhist | random | relax | 5 | 1000 | 13.020 ± 3.730 | 0.080 ± 0.018 | 0.027 ± 0.025 | 0.932 ± 0.011 | 42.800 ± 2.159 | 0.751 ± 0.014 |

## MHIST: exact integer counts vs LP relaxation

| set | pct_relax_above_exact | mean_rel_diff |
|---|---|---|
| mined_last_epoch | 0.0000 | 0.0000 |
| random | 0.0000 | 0.0000 |

## Share of tuples with a gap, by number of split-vote images in the tuple (pooled over runs)


### mined_last_epoch

| dataset | model | n_split | n | pct_gap |
|---|---|---|---|---|
| gleason | relax | 0 | 1028 | 0.0 |
| gleason | relax | 1 | 2811 | 0.0 |
| gleason | relax | 2 | 2632 | 0.0 |
| gleason | relax | 3 | 945 | 75.9 |
| gleason | relax | 4 | 104 | 98.1 |
| mhist | exact | 0 | 14 | 0.0 |
| mhist | exact | 1 | 85 | 0.0 |
| mhist | exact | 2 | 306 | 0.0 |
| mhist | exact | 3 | 424 | 17.2 |
| mhist | exact | 4 | 291 | 59.1 |
| mhist | relax | 0 | 14 | 0.0 |
| mhist | relax | 1 | 85 | 0.0 |
| mhist | relax | 2 | 306 | 0.0 |
| mhist | relax | 3 | 424 | 17.2 |
| mhist | relax | 4 | 291 | 59.1 |

### random

| dataset | model | n_split | n | pct_gap |
|---|---|---|---|---|
| gleason | relax | 0 | 2546 | 0.0 |
| gleason | relax | 1 | 6163 | 0.0 |
| gleason | relax | 2 | 4803 | 0.0 |
| gleason | relax | 3 | 1382 | 75.8 |
| gleason | relax | 4 | 106 | 100.0 |
| mhist | exact | 0 | 67 | 0.0 |
| mhist | exact | 1 | 578 | 0.0 |
| mhist | exact | 2 | 1646 | 0.0 |
| mhist | exact | 3 | 1877 | 12.6 |
| mhist | exact | 4 | 832 | 49.8 |
| mhist | relax | 0 | 67 | 0.0 |
| mhist | relax | 1 | 578 | 0.0 |
| mhist | relax | 2 | 1646 | 0.0 |
| mhist | relax | 3 | 1877 | 12.6 |
| mhist | relax | 4 | 832 | 49.8 |

## Largest gaps, MHIST mined tuples, exact counts (pairs in order ap an ac pn pc nc)

| run | q_a | q_p | q_n | q_c | t_ap | t_an | t_ac | t_pn | t_pc | t_nc | exact_s_ind | exact_s_joint | exact_L_ind | exact_L_joint | exact_rel_gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| f2s2_hsrl | 0.571 | 0.571 | 0.429 | 0.429 | 0.944 | 0.106 | 0.106 | 0.129 | 0.106 | 0.945 | 0.143 0.857 0.857 0.857 0.857 0.143 | 0.143 0.857 0.286 0.000 0.857 0.143 | 0.707 | 0.526 | 0.256 |
| f1s1_hsrl | 0.571 | 0.571 | 0.429 | 0.286 | 0.967 | 0.147 | 0.175 | 0.141 | 0.176 | 0.803 | 0.143 0.857 0.714 0.857 0.714 0.286 | 0.143 0.286 0.714 0.857 0.429 0.571 | 0.587 | 0.460 | 0.216 |
| f1s1_hsrl | 0.571 | 0.571 | 0.429 | 0.286 | 0.967 | 0.141 | 0.176 | 0.147 | 0.175 | 0.803 | 0.143 0.857 0.714 0.857 0.714 0.286 | 0.143 0.857 0.429 0.286 0.714 0.571 | 0.587 | 0.460 | 0.216 |

## Reading fixed in advance (ASSUMPTIONS D44)

Primary: MHIST, mined tuples, exact counts, mean over 5 draws. The joint loss has something to act on if the joint worst case is below the independent one in >= 10% of tuples AND those gaps average >= 5% of the loss.

- tuples with a gap: 21.9% · mean relative gap where there is one: 8.1%
- **criterion met: True**
