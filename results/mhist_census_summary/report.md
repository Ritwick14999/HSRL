# Tuple census across folds (hsrl, 5 runs)

Counts-only bounds assume a common reader panel (not strictly true for Gleason). Linked verdicts skip pairs with < 3 shared readers. Set A (random tuples) depends only on the fold's labelled set, so it is identical across seeds within a fold.

## Set A: 100k random role-valid tuples, per fold (%)

| fold | term | ordering | pct_certified | pct_contradicted | pct_undecided | pct_supported | pct_violated | pct_tie | pct_linked_violated_given_undecided | pct_linked_violated_given_certified | pct_linked_violated_given_contradicted |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | s_ap > s_an | 85.900 | 0.000 | 14.100 | nan | nan | nan | nan | nan | nan |
| 0 | 2 | s_ap > s_nc | 19.600 | 17.200 | 63.200 | nan | nan | nan | nan | nan | nan |
| 0 | 3 | s_ap > s_ac | 85.800 | 0.000 | 14.200 | nan | nan | nan | nan | nan | nan |
| 1 | 1 | s_ap > s_an | 86.300 | 0.000 | 13.700 | nan | nan | nan | nan | nan | nan |
| 1 | 2 | s_ap > s_nc | 23.700 | 20.700 | 55.700 | nan | nan | nan | nan | nan | nan |
| 1 | 3 | s_ap > s_ac | 86.300 | 0.000 | 13.700 | nan | nan | nan | nan | nan | nan |
| 2 | 1 | s_ap > s_an | 85.100 | 0.000 | 14.900 | nan | nan | nan | nan | nan | nan |
| 2 | 2 | s_ap > s_nc | 20.100 | 19.500 | 60.400 | nan | nan | nan | nan | nan | nan |
| 2 | 3 | s_ap > s_ac | 85.200 | 0.000 | 14.800 | nan | nan | nan | nan | nan | nan |
| 3 | 1 | s_ap > s_an | 82.600 | 0.000 | 17.400 | nan | nan | nan | nan | nan | nan |
| 3 | 2 | s_ap > s_nc | 20.700 | 16.700 | 62.500 | nan | nan | nan | nan | nan | nan |
| 3 | 3 | s_ap > s_ac | 82.800 | 0.000 | 17.200 | nan | nan | nan | nan | nan | nan |
| 4 | 1 | s_ap > s_an | 80.200 | 0.000 | 19.800 | nan | nan | nan | nan | nan | nan |
| 4 | 2 | s_ap > s_nc | 16.500 | 14.000 | 69.500 | nan | nan | nan | nan | nan | nan |
| 4 | 3 | s_ap > s_ac | 80.100 | 0.000 | 19.900 | nan | nan | nan | nan | nan | nan |

## Set B: mined tuples (mean ± std over runs, %)

| set | term | runs | pct_certified | pct_contradicted | pct_undecided | pct_supported | pct_violated | pct_tie | pct_linked_violated_given_undecided | pct_linked_violated_given_certified | pct_linked_violated_given_contradicted | skipped_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B_mined_epoch0 | 1 | 5 | 80.714 ± 4.686 | 0.000 ± 0.000 | 19.286 ± 4.686 | nan | nan | nan | nan | nan | nan | 100.000 ± 0.000 |
| B_mined_epoch0 | 2 | 5 | 15.625 ± 4.553 | 16.786 ± 4.773 | 67.589 ± 8.320 | nan | nan | nan | nan | nan | nan | 100.000 ± 0.000 |
| B_mined_epoch0 | 3 | 5 | 80.625 ± 5.491 | 0.000 ± 0.000 | 19.375 ± 5.491 | nan | nan | nan | nan | nan | nan | 100.000 ± 0.000 |
| B_mined_epoch29 | 1 | 5 | 78.929 ± 7.304 | 0.000 ± 0.000 | 21.071 ± 7.304 | nan | nan | nan | nan | nan | nan | 100.000 ± 0.000 |
| B_mined_epoch29 | 2 | 5 | 17.500 ± 6.976 | 12.589 ± 7.426 | 69.911 ± 12.677 | nan | nan | nan | nan | nan | nan | 100.000 ± 0.000 |
| B_mined_epoch29 | 3 | 5 | 78.304 ± 6.207 | 0.000 ± 0.000 | 21.696 ± 6.207 | nan | nan | nan | nan | nan | nan | 100.000 ± 0.000 |

## Pseudo-label errors vs tuple status: PATCH LEVEL (secondary)

AUROC of the mean violation / undecided rate of the 5 nearest labelled patches (Stage I embedding) for predicting a wrong accepted pseudo-label; overall and within unanimous / split-vote patches. Patch-level p-values are optimistic (patches within a core are correlated) and are not aggregated here.

| measure | all runs | fold 0 | fold 1 | fold 2 | fold 3 | fold 4 |
|---|---|---|---|---|---|---|
| n_accepted | 1222.600 ± 38.863 | 1204.000 | 1283.000 | 1179.000 | 1215.000 | 1232.000 |
| n_wrong | 109.400 ± 8.019 | 108.000 | 111.000 | 97.000 | 119.000 | 112.000 |
| err_unanimous | 0.022 ± 0.009 | 0.019 | 0.010 | 0.022 | 0.026 | 0.034 |
| err_split | 0.133 ± 0.010 | 0.136 | 0.133 | 0.120 | 0.148 | 0.127 |
| nbr_undecided_rate_auroc | 0.642 ± 0.054 | 0.678 | 0.622 | 0.690 | 0.662 | 0.556 |
| nbr_undecided_rate_auroc_unanimous | 0.675 ± 0.112 | 0.660 | 0.763 | 0.733 | 0.730 | 0.487 |
| nbr_undecided_rate_auroc_split_vote | 0.621 ± 0.053 | 0.664 | 0.594 | 0.666 | 0.641 | 0.541 |
