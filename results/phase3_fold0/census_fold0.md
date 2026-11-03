# Phase 4: tuple census, fold 0 seed 0

Script: `analysis/tuple_census.py`. Raw outputs: `results/<run>/census/`. Assumptions A4.1–A4.6.

Caveat: the counts-only bounds assume a common reader panel. Gleason readers vary per core and per patch (mean ~3.4 shared readers per pair).

## Verdicts per term

| run | set | term | ordering | pct_certified | pct_contradicted | pct_undecided | n_linked_evaluable | n_linked_skipped | pct_supported | pct_violated | pct_tie | pct_linked_violated_given_undecided | pct_linked_violated_given_certified | pct_linked_violated_given_contradicted |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| f0s0_hsrl | A_random | 1 | s_ap > s_an | 96.9 | 0.0 | 3.1 | 80758 | 19242 | 96.0 | 1.4 | 2.6 | 27.7 | 0.6 | nan |
| f0s0_hsrl | A_random | 2 | s_ap > s_nc | 35.5 | 27.6 | 36.9 | 77277 | 22723 | 34.8 | 27.9 | 37.3 | 13.0 | 0.8 | 82.8 |
| f0s0_hsrl | A_random | 3 | s_ap > s_ac | 96.9 | 0.0 | 3.1 | 80619 | 19381 | 96.0 | 1.4 | 2.5 | 28.3 | 0.6 | nan |
| f0s0_hsrl | B_mined_epoch0 | 1 | s_ap > s_an | 97.9 | 0.0 | 2.1 | 409 | 103 | 95.4 | 2.0 | 2.7 | 50.0 | 1.2 | nan |
| f0s0_hsrl | B_mined_epoch0 | 2 | s_ap > s_nc | 33.0 | 31.4 | 35.5 | 396 | 116 | 33.6 | 29.5 | 36.9 | 11.3 | 2.2 | 79.8 |
| f0s0_hsrl | B_mined_epoch0 | 3 | s_ap > s_ac | 96.9 | 0.0 | 3.1 | 409 | 103 | 95.8 | 1.2 | 2.9 | 15.4 | 0.8 | nan |
| f0s0_hsrl | B_mined_epoch29 | 1 | s_ap > s_an | 94.5 | 0.0 | 5.5 | 389 | 123 | 94.9 | 1.3 | 3.9 | 11.1 | 0.8 | nan |
| f0s0_hsrl | B_mined_epoch29 | 2 | s_ap > s_nc | 37.9 | 29.5 | 32.6 | 370 | 142 | 32.2 | 27.3 | 40.5 | 7.9 | 0.0 | 81.2 |
| f0s0_hsrl | B_mined_epoch29 | 3 | s_ap > s_ac | 96.7 | 0.0 | 3.3 | 405 | 107 | 97.0 | 0.5 | 2.5 | 7.1 | 0.3 | nan |
| f0s0_hsrl_no_t2 | A_random | 1 | s_ap > s_an | 96.9 | 0.0 | 3.1 | 80758 | 19242 | 96.0 | 1.4 | 2.6 | 27.7 | 0.6 | nan |
| f0s0_hsrl_no_t2 | A_random | 2 | s_ap > s_nc | 35.5 | 27.6 | 36.9 | 77277 | 22723 | 34.8 | 27.9 | 37.3 | 13.0 | 0.8 | 82.8 |
| f0s0_hsrl_no_t2 | A_random | 3 | s_ap > s_ac | 96.9 | 0.0 | 3.1 | 80619 | 19381 | 96.0 | 1.4 | 2.5 | 28.3 | 0.6 | nan |
| f0s0_hsrl_no_t2 | B_mined_epoch0 | 1 | s_ap > s_an | 97.9 | 0.0 | 2.1 | 405 | 107 | 95.3 | 2.2 | 2.5 | 50.0 | 1.5 | nan |
| f0s0_hsrl_no_t2 | B_mined_epoch0 | 2 | s_ap > s_nc | 34.2 | 31.2 | 34.6 | 392 | 120 | 34.2 | 30.9 | 34.9 | 11.8 | 2.1 | 82.4 |
| f0s0_hsrl_no_t2 | B_mined_epoch0 | 3 | s_ap > s_ac | 97.3 | 0.0 | 2.7 | 411 | 101 | 95.4 | 1.5 | 3.2 | 33.3 | 0.7 | nan |
| f0s0_hsrl_no_t2 | B_mined_epoch29 | 1 | s_ap > s_an | 95.7 | 0.0 | 4.3 | 407 | 105 | 96.3 | 1.0 | 2.7 | 12.5 | 0.5 | nan |
| f0s0_hsrl_no_t2 | B_mined_epoch29 | 2 | s_ap > s_nc | 34.4 | 26.0 | 39.6 | 431 | 81 | 34.1 | 26.2 | 39.7 | 16.1 | 0.6 | 79.6 |
| f0s0_hsrl_no_t2 | B_mined_epoch29 | 3 | s_ap > s_ac | 94.7 | 0.0 | 5.3 | 427 | 85 | 95.3 | 1.4 | 3.3 | 25.0 | 0.2 | nan |

## Mined tuples: hinge active vs linked verdict

| run | set | term | hinge | n | n_evaluable | pct_violated | pct_supported |
|---|---|---|---|---|---|---|---|
| f0s0_hsrl | B_mined_epoch0 | 1 | active | 512 | 409 | 2.0 | 95.4 |
| f0s0_hsrl | B_mined_epoch0 | 1 | inactive | 0 | 0 | nan | nan |
| f0s0_hsrl | B_mined_epoch0 | 2 | active | 512 | 396 | 29.5 | 33.6 |
| f0s0_hsrl | B_mined_epoch0 | 2 | inactive | 0 | 0 | nan | nan |
| f0s0_hsrl | B_mined_epoch0 | 3 | active | 512 | 409 | 1.2 | 95.8 |
| f0s0_hsrl | B_mined_epoch0 | 3 | inactive | 0 | 0 | nan | nan |
| f0s0_hsrl | B_mined_epoch29 | 1 | active | 512 | 389 | 1.3 | 94.9 |
| f0s0_hsrl | B_mined_epoch29 | 1 | inactive | 0 | 0 | nan | nan |
| f0s0_hsrl | B_mined_epoch29 | 2 | active | 512 | 370 | 27.3 | 32.2 |
| f0s0_hsrl | B_mined_epoch29 | 2 | inactive | 0 | 0 | nan | nan |
| f0s0_hsrl | B_mined_epoch29 | 3 | active | 512 | 405 | 0.5 | 97.0 |
| f0s0_hsrl | B_mined_epoch29 | 3 | inactive | 0 | 0 | nan | nan |
| f0s0_hsrl_no_t2 | B_mined_epoch0 | 1 | active | 512 | 405 | 2.2 | 95.3 |
| f0s0_hsrl_no_t2 | B_mined_epoch0 | 1 | inactive | 0 | 0 | nan | nan |
| f0s0_hsrl_no_t2 | B_mined_epoch0 | 2 | active | 512 | 392 | 30.9 | 34.2 |
| f0s0_hsrl_no_t2 | B_mined_epoch0 | 2 | inactive | 0 | 0 | nan | nan |
| f0s0_hsrl_no_t2 | B_mined_epoch0 | 3 | active | 512 | 411 | 1.5 | 95.4 |
| f0s0_hsrl_no_t2 | B_mined_epoch0 | 3 | inactive | 0 | 0 | nan | nan |
| f0s0_hsrl_no_t2 | B_mined_epoch29 | 1 | active | 80 | 63 | 1.6 | 95.2 |
| f0s0_hsrl_no_t2 | B_mined_epoch29 | 1 | inactive | 432 | 344 | 0.9 | 96.5 |
| f0s0_hsrl_no_t2 | B_mined_epoch29 | 2 | active | 325 | 283 | 20.1 | 38.2 |
| f0s0_hsrl_no_t2 | B_mined_epoch29 | 2 | inactive | 187 | 148 | 37.8 | 26.4 |
| f0s0_hsrl_no_t2 | B_mined_epoch29 | 3 | active | 8 | 7 | 0.0 | 100.0 |
| f0s0_hsrl_no_t2 | B_mined_epoch29 | 3 | inactive | 504 | 420 | 1.4 | 95.2 |

## Wrong-but-confident pseudo-labels vs violated/undecided tuples (f0s0_hsrl)

```json
{
 "n_accepted_nontie": 3133,
 "n_wrong_confident": 268,
 "nbr_viol_rate": {
  "mean_wrong": 0.08830358456091714,
  "mean_correct": 0.07430155172919597,
  "auroc_predicting_wrong": 0.681153786043604,
  "perm_p": 0.0,
  "within_unanimous": {
   "n": 2410,
   "n_wrong": 119,
   "auroc_predicting_wrong": 0.724482721940806,
   "perm_p": 0.0
  },
  "within_split_vote": {
   "n": 723,
   "n_wrong": 149,
   "auroc_predicting_wrong": 0.5625540771227463,
   "perm_p": 0.017
  }
 },
 "nbr_undecided_rate": {
  "mean_wrong": 0.14495108994973385,
  "mean_correct": 0.13586391623253685,
  "auroc_predicting_wrong": 0.653422025995676,
  "perm_p": 0.0,
  "within_unanimous": {
   "n": 2410,
   "n_wrong": 119,
   "auroc_predicting_wrong": 0.7083894229887502,
   "perm_p": 0.0
  },
  "within_split_vote": {
   "n": 723,
   "n_wrong": 149,
   "auroc_predicting_wrong": 0.5179302200500432,
   "perm_p": 0.4995
  }
 },
 "nbr_label_disagree": {
  "mean_wrong": 0.020149253731343283,
  "mean_correct": 0.00886561954624782,
  "auroc_predicting_wrong": 0.5260555859446224,
  "perm_p": 0.001,
  "within_unanimous": {
   "n": 2410,
   "n_wrong": 119,
   "auroc_predicting_wrong": 0.5413308928984077,
   "perm_p": 0.0
  },
  "within_split_vote": {
   "n": 723,
   "n_wrong": 149,
   "auroc_predicting_wrong": 0.5039052451885976,
   "perm_p": 0.793
  }
 },
 "core_level": {
  "n_cores": 113,
  "spearman_err_vs_viol_rate": 0.32973401079271636,
  "spearman_err_vs_undecided_rate": 0.24665604014412712
 },
 "error_rate_unanimous": 0.04937759336099585,
 "error_rate_split_vote": 0.20608575380359612
}
```
