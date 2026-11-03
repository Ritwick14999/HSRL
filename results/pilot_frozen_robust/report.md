# EXPLORATORY PILOT, robustness checks (secondary to the pre-registered result)

## Consistent reader renaming (should be 0)

| variant | pairs | max |Δ bal acc| | max |Δ Brier| |
|---|---|---|---|
| interval | 15 | 0.000 | 0.000 |
| worstcase | 15 | 0.000 | 0.000 |

## Linked vs repeated permutation draws

| variant | vs | metric | Δ linked − permuted | pairs ≥ +1pt | folds ≥ +1pt | meets standard |
|---|---|---|---|---|---|---|
| interval | interval_permuted_p0 | bal acc | -0.001 | 0 | 0 | False |
| interval | interval_permuted_p0 | split-vote acc | -0.002 | 1 | 0 | False |
| interval | interval_permuted_p1 | bal acc | -0.002 | 0 | 0 | False |
| interval | interval_permuted_p1 | split-vote acc | -0.003 | 1 | 0 | False |
| interval | interval_permuted_p2 | bal acc | 0.000 | 1 | 0 | False |
| interval | interval_permuted_p2 | split-vote acc | -0.001 | 0 | 0 | False |
| interval | interval_permuted_p3 | bal acc | -0.002 | 0 | 0 | False |
| interval | interval_permuted_p3 | split-vote acc | -0.008 | 0 | 0 | False |
| interval | interval_permuted_p4 | bal acc | -0.002 | 0 | 0 | False |
| interval | interval_permuted_p4 | split-vote acc | -0.004 | 0 | 0 | False |
| interval | interval_permuted_mean | bal acc | -0.001 | 0 | 0 | False |
| interval | interval_permuted_mean | split-vote acc | -0.004 | 0 | 0 | False |
| worstcase | worstcase_permuted_p0 | bal acc | -0.001 | 0 | 0 | False |
| worstcase | worstcase_permuted_p0 | split-vote acc | -0.004 | 0 | 0 | False |
| worstcase | worstcase_permuted_p1 | bal acc | 0.000 | 0 | 0 | False |
| worstcase | worstcase_permuted_p1 | split-vote acc | -0.001 | 1 | 0 | False |
| worstcase | worstcase_permuted_p2 | bal acc | -0.001 | 0 | 0 | False |
| worstcase | worstcase_permuted_p2 | split-vote acc | -0.004 | 0 | 0 | False |
| worstcase | worstcase_permuted_p3 | bal acc | -0.001 | 0 | 0 | False |
| worstcase | worstcase_permuted_p3 | split-vote acc | -0.004 | 0 | 0 | False |
| worstcase | worstcase_permuted_p4 | bal acc | -0.001 | 0 | 0 | False |
| worstcase | worstcase_permuted_p4 | split-vote acc | -0.004 | 0 | 0 | False |
| worstcase | worstcase_permuted_mean | bal acc | -0.001 | 0 | 0 | False |
| worstcase | worstcase_permuted_mean | split-vote acc | -0.003 | 0 | 0 | False |
