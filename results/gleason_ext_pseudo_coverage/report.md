# Pseudo-label precision at equal coverage / coverage at equal precision

Runs: 48 (all runs with a saved Stage III pseudo-label file). Pool = vote-filtered unlabelled split of the fold, identical for every config. Precision vs hidden majority labels (non-tie). Coverage at precision p = largest accepted fraction whose precision is still >= p (top-k by confidence, k >= 50). split_share = fraction of split-vote patches among accepted non-tie patches. tau_* = the actual operating point at tau = 0.85.

## Mean ± std per config

| config | runs | prec@cov0.3 | split_share@cov0.3 | prec@cov0.5 | split_share@cov0.5 | prec@cov0.7 | split_share@cov0.7 | prec@cov0.8 | split_share@cov0.8 | cov@prec0.90 | cov@prec0.93 | cov@prec0.95 | tau_coverage | tau_precision |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hsrl_soft | 15 | 0.970 ± 0.018 | 0.125 ± 0.023 | 0.932 ± 0.033 | 0.189 ± 0.025 | 0.888 ± 0.043 | 0.244 ± 0.023 | 0.865 ± 0.045 | 0.267 ± 0.022 | 0.671 ± 0.168 | 0.548 ± 0.155 | 0.453 ± 0.133 | 0.459 ± 0.098 | 0.947 ± 0.011 |
| hsrl_soft_s1e60 | 15 | 0.980 ± 0.008 | 0.111 ± 0.019 | 0.956 ± 0.013 | 0.177 ± 0.020 | 0.922 ± 0.017 | 0.239 ± 0.019 | 0.898 ± 0.018 | 0.266 ± 0.019 | 0.795 ± 0.074 | 0.662 ± 0.078 | 0.548 ± 0.082 | 0.511 ± 0.042 | 0.955 ± 0.009 |
| supported_counts | 6 | 0.982 ± 0.008 | 0.107 ± 0.014 | 0.957 ± 0.013 | 0.178 ± 0.020 | 0.919 ± 0.015 | 0.239 ± 0.022 | 0.894 ± 0.017 | 0.266 ± 0.021 | 0.779 ± 0.069 | 0.649 ± 0.073 | 0.543 ± 0.074 | 0.520 ± 0.050 | 0.954 ± 0.011 |
| supported_linked | 6 | 0.978 ± 0.009 | 0.118 ± 0.010 | 0.954 ± 0.012 | 0.182 ± 0.014 | 0.917 ± 0.016 | 0.241 ± 0.016 | 0.893 ± 0.018 | 0.268 ± 0.017 | 0.776 ± 0.075 | 0.635 ± 0.079 | 0.534 ± 0.074 | 0.521 ± 0.040 | 0.951 ± 0.012 |
| supported_permuted | 6 | 0.981 ± 0.006 | 0.109 ± 0.013 | 0.953 ± 0.013 | 0.179 ± 0.015 | 0.917 ± 0.016 | 0.240 ± 0.019 | 0.894 ± 0.018 | 0.266 ± 0.020 | 0.773 ± 0.074 | 0.636 ± 0.080 | 0.523 ± 0.077 | 0.521 ± 0.050 | 0.951 ± 0.009 |

## Paired differences (same fold and seed)

CI = t-interval over pairs (optimistic: 3 test folds). Positive = first config higher.

| comparison | metric | n_pairs | mean_diff | ci95_lo | ci95_hi | a_higher | per_fold_mean | folds_same_sign |
|---|---|---|---|---|---|---|---|---|
| supported_linked − hsrl_soft | prec@cov0.3 | 6 | 0.008 | -0.007 | 0.024 | 4/6 | f0:+0.003 / f1:+0.025 / f2:-0.003 | 2 |
| supported_linked − hsrl_soft | prec@cov0.5 | 6 | 0.021 | -0.001 | 0.044 | 5/6 | f0:+0.013 / f1:+0.048 / f2:+0.004 | 3 |
| supported_linked − hsrl_soft | prec@cov0.7 | 6 | 0.027 | -0.001 | 0.055 | 5/6 | f0:+0.022 / f1:+0.057 / f2:+0.002 | 3 |
| supported_linked − hsrl_soft | prec@cov0.8 | 6 | 0.027 | 0.002 | 0.052 | 5/6 | f0:+0.023 / f1:+0.054 / f2:+0.004 | 3 |
| supported_linked − hsrl_soft | cov@prec0.90 | 6 | 0.111 | 0.019 | 0.203 | 6/6 | f0:+0.090 / f1:+0.212 / f2:+0.031 | 3 |
| supported_linked − hsrl_soft | cov@prec0.93 | 6 | 0.093 | 0.003 | 0.183 | 5/6 | f0:+0.082 / f1:+0.187 / f2:+0.010 | 3 |
| supported_linked − hsrl_soft | cov@prec0.95 | 6 | 0.088 | -0.001 | 0.178 | 5/6 | f0:+0.074 / f1:+0.176 / f2:+0.015 | 3 |
| supported_linked − hsrl_soft | split_share@cov0.5 | 6 | -0.008 | -0.026 | 0.010 | 2/6 | f0:+0.013 / f1:-0.022 / f2:-0.015 | 2 |
| supported_permuted − hsrl_soft | prec@cov0.3 | 6 | 0.012 | -0.005 | 0.028 | 5/6 | f0:+0.004 / f1:+0.031 / f2:+0.000 | 3 |
| supported_permuted − hsrl_soft | prec@cov0.5 | 6 | 0.020 | -0.003 | 0.042 | 5/6 | f0:+0.014 / f1:+0.046 / f2:-0.001 | 2 |
| supported_permuted − hsrl_soft | prec@cov0.7 | 6 | 0.027 | -0.001 | 0.055 | 5/6 | f0:+0.024 / f1:+0.058 / f2:+0.000 | 3 |
| supported_permuted − hsrl_soft | prec@cov0.8 | 6 | 0.028 | 0.002 | 0.053 | 6/6 | f0:+0.026 / f1:+0.056 / f2:+0.002 | 3 |
| supported_permuted − hsrl_soft | cov@prec0.90 | 6 | 0.108 | 0.014 | 0.201 | 6/6 | f0:+0.098 / f1:+0.210 / f2:+0.015 | 3 |
| supported_permuted − hsrl_soft | cov@prec0.93 | 6 | 0.094 | 0.006 | 0.183 | 5/6 | f0:+0.094 / f1:+0.185 / f2:+0.004 | 3 |
| supported_permuted − hsrl_soft | cov@prec0.95 | 6 | 0.078 | -0.011 | 0.167 | 4/6 | f0:+0.078 / f1:+0.167 / f2:-0.011 | 2 |
| supported_permuted − hsrl_soft | split_share@cov0.5 | 6 | -0.011 | -0.024 | 0.002 | 2/6 | f0:+0.004 / f1:-0.021 / f2:-0.017 | 2 |
| supported_counts − hsrl_soft | prec@cov0.3 | 6 | 0.013 | -0.003 | 0.028 | 5/6 | f0:+0.007 / f1:+0.031 / f2:+0.000 | 3 |
| supported_counts − hsrl_soft | prec@cov0.5 | 6 | 0.024 | 0.001 | 0.046 | 5/6 | f0:+0.022 / f1:+0.048 / f2:+0.001 | 3 |
| supported_counts − hsrl_soft | prec@cov0.7 | 6 | 0.029 | -0.000 | 0.059 | 5/6 | f0:+0.024 / f1:+0.060 / f2:+0.003 | 3 |
| supported_counts − hsrl_soft | prec@cov0.8 | 6 | 0.029 | 0.001 | 0.056 | 5/6 | f0:+0.023 / f1:+0.057 / f2:+0.005 | 3 |
| supported_counts − hsrl_soft | cov@prec0.90 | 6 | 0.114 | 0.013 | 0.215 | 5/6 | f0:+0.089 / f1:+0.224 / f2:+0.029 | 3 |
| supported_counts − hsrl_soft | cov@prec0.93 | 6 | 0.107 | 0.013 | 0.202 | 5/6 | f0:+0.106 / f1:+0.201 / f2:+0.014 | 3 |
| supported_counts − hsrl_soft | cov@prec0.95 | 6 | 0.098 | 0.012 | 0.184 | 5/6 | f0:+0.115 / f1:+0.176 / f2:+0.004 | 3 |
| supported_counts − hsrl_soft | split_share@cov0.5 | 6 | -0.012 | -0.025 | 0.001 | 1/6 | f0:-0.001 / f1:-0.015 / f2:-0.022 | 3 |
| supported_linked − supported_permuted | prec@cov0.3 | 6 | -0.003 | -0.007 | 0.001 | 2/6 | f0:-0.001 / f1:-0.006 / f2:-0.003 | 3 |
| supported_linked − supported_permuted | prec@cov0.5 | 6 | 0.002 | -0.003 | 0.007 | 5/6 | f0:-0.001 / f1:+0.002 / f2:+0.005 | 2 |
| supported_linked − supported_permuted | prec@cov0.7 | 6 | -0.000 | -0.006 | 0.006 | 3/6 | f0:-0.001 / f1:-0.001 / f2:+0.001 | 2 |
| supported_linked − supported_permuted | prec@cov0.8 | 6 | -0.001 | -0.005 | 0.003 | 2/6 | f0:-0.003 / f1:-0.002 / f2:+0.002 | 2 |
| supported_linked − supported_permuted | cov@prec0.90 | 6 | 0.003 | -0.021 | 0.028 | 3/6 | f0:-0.008 / f1:+0.002 / f2:+0.017 | 2 |
| supported_linked − supported_permuted | cov@prec0.93 | 6 | -0.001 | -0.026 | 0.024 | 2/6 | f0:-0.012 / f1:+0.003 / f2:+0.006 | 1 |
| supported_linked − supported_permuted | cov@prec0.95 | 6 | 0.010 | -0.026 | 0.046 | 4/6 | f0:-0.004 / f1:+0.009 / f2:+0.026 | 2 |
| supported_linked − supported_permuted | split_share@cov0.5 | 6 | 0.003 | -0.006 | 0.012 | 4/6 | f0:+0.009 / f1:-0.002 / f2:+0.002 | 2 |
