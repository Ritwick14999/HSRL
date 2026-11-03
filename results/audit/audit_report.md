# Audit report

## 1. Completeness
- main/supervised: 15/15 complete
- main/hsrl: 15/15 complete
- main/hsrl_no_t2: 15/15 complete
- main/hsrl_no_stage1: 15/15 complete
- deviations/hsrl_s1e60: 15/15 complete
- deviations/hsrl_no_t2_s1e60: 15/15 complete
- deviations/supervised_e65: 15/15 complete
- soft/supervised_soft: 15/15 complete
- soft/supervised_soft_e65: 15/15 complete
- soft/hsrl_soft: 15/15 complete
- soft/hsrl_soft_s1e60: 15/15 complete
- excl_r1/supervised: 15/15 complete
- excl_r1/supervised_soft: 15/15 complete
- excl_r1/hsrl: 15/15 complete
- excl_r1/hsrl_soft: 15/15 complete
- excl_r4/supervised: 15/15 complete
- excl_r4/supervised_soft: 15/15 complete
- excl_r4/hsrl: 15/15 complete
- excl_r4/hsrl_soft: 15/15 complete
- p1024/supervised: 15/15 complete
- p1024/hsrl: 15/15 complete
- p1024/hsrl_no_t2: 15/15 complete
- p1024/hsrl_no_stage1: 15/15 complete
- deviations/hsrl_boundary (fold 0): 3/3 complete
**Completeness problems: 0**

## 2. Metrics recomputed from saved predictions
- 25 random runs; largest |difference| in balanced accuracy or Brier: **0.00005** (metrics.json is rounded to 4 d.p.)

## 3. Headline numbers recomputed from metrics.json
- main/supervised: acc 0.793, bal acc 0.781, Brier 0.171, split acc 0.662
- main/hsrl: acc 0.795, bal acc 0.773, Brier 0.160, split acc 0.652
- main/hsrl_no_t2: acc 0.802, bal acc 0.782, Brier 0.158, split acc 0.656
- main/hsrl_no_stage1: acc 0.768, bal acc 0.747, Brier 0.165, split acc 0.632
- paired HSRL − supervised: bal acc -0.007 (4/15 better), Brier -0.011 (15/15 better)
- paired HSRL 60 ep − supervised 65 ep: bal acc +0.003
- 1024 px: HSRL bal acc 0.810 vs supervised 0.811

## 4. Split integrity per label set
- p512/labels_benign-drop: OK (8897 patches; no core in two splits; test slides disjoint; each slide tested once; labelled only from train; unlabelled/val/test files carry no votes)
- p512/labels_benign-drop_excl-r1: OK (7212 patches; no core in two splits; test slides disjoint; each slide tested once; labelled only from train; unlabelled/val/test files carry no votes)
- p512/labels_benign-drop_excl-r4: OK (7471 patches; no core in two splits; test slides disjoint; each slide tested once; labelled only from train; unlabelled/val/test files carry no votes)
- p1024/labels_benign-drop: OK (2090 patches; no core in two splits; test slides disjoint; each slide tested once; labelled only from train; unlabelled/val/test files carry no votes)

## 5. Hidden-label access (eval_labels) call sites
- analysis/class_shift.py:41: `cache[key] = load_dataset(cfg).eval_labels("test")[["patch_id", "majority_label", "tie", "unanimous"]]`
- analysis/pseudo_coverage.py:102: `label_cache[key] = load_dataset(rc).eval_labels("unlabelled")[["patch_id", "majority_label", "tie", "unanimous`
- analysis/tsne.py:81: `lab = data.eval_labels("test").set_index("patch_id").loc[test.patch_id]   # evaluation only`
- analysis/tuple_census.py:250: `hidden = data.eval_labels("unlabelled")[["patch_id", "core_id", "majority_label", "tie", "unanimous"]]`
- hsrl/data/base.py:7: `eval_labels(split)  ground-truth / vote table for evaluation and analysis only`
- hsrl/data/base.py:40: `return self._eval_labels(split)`
- hsrl/pilot_frozen.py:186: `test_lab = data.eval_labels("test")                                      # evaluation only`
- hsrl/train.py:50: `y = ctx.data.eval_labels("val").set_index("patch_id").loc[self.val.patch_id]`
- hsrl/train.py:124: `out[split] = evaluate_predictions(preds, ctx.data.eval_labels(split))`
- hsrl/train.py:169: `unl_labels = data.eval_labels("unlabelled")`
All call sites must be evaluation, monitoring or post-hoc analysis; none may be in hsrl/stages.py.
- hsrl/stages.py reads hidden labels: **no**

## 6. Stage I reuse pointers
- 60 reused runs checked, mismatches: **0**

## 7. Pilot criterion recomputed independently
- overall_bal_acc: interval_counts_only vs annotator_aware: mean -0.0021, pairs ≥ +1pt 1/15, meets: False
- overall_bal_acc: interval_linked vs annotator_aware: mean +0.0037, pairs ≥ +1pt 2/15, meets: False
- overall_bal_acc: interval_permuted vs annotator_aware: mean +0.0043, pairs ≥ +1pt 3/15, meets: False
- overall_bal_acc: worstcase_counts_only vs annotator_aware: mean +0.0031, pairs ≥ +1pt 1/15, meets: False
- overall_bal_acc: worstcase_linked vs annotator_aware: mean +0.0047, pairs ≥ +1pt 2/15, meets: False
- overall_bal_acc: worstcase_permuted vs annotator_aware: mean +0.0057, pairs ≥ +1pt 2/15, meets: False
- split_vote_acc: interval_counts_only vs probe_hard: mean -0.0325, pairs ≥ +1pt 0/15, meets: False
- split_vote_acc: interval_linked vs probe_hard: mean -0.0247, pairs ≥ +1pt 0/15, meets: False
- split_vote_acc: interval_permuted vs probe_hard: mean -0.0227, pairs ≥ +1pt 0/15, meets: False
- split_vote_acc: worstcase_counts_only vs probe_hard: mean -0.0205, pairs ≥ +1pt 0/15, meets: False
- split_vote_acc: worstcase_linked vs probe_hard: mean -0.0230, pairs ≥ +1pt 0/15, meets: False
- split_vote_acc: worstcase_permuted vs probe_hard: mean -0.0191, pairs ≥ +1pt 1/15, meets: False