# ASSUMPTIONS.md

Every choice that the HSRL paper (ACCV 2026 #936) or the task does not fix, with a justification.
Items marked **[pending]** wait for the user's confirmation.

## Data (Phase 0)
- **A0.1 Data location.** Raw data is `data/gleason/` (not `data/gleason2019/`). Training images extracted to
  `data/gleason/TrainImgs/`; map k extracted to `data/gleason/Map{k}/`. *Why:* the actual folder layout found on disk.
- **A0.2 core_id = `slide{SSS}_core{CCC}`, group = slide.** Taken from the file names. Patient IDs are not released.
  *Why:* slide is the only grouping recoverable from the data.
- **A0.3 Orphan masks excluded.** `slide007_core137` and `slide007_core145` (Maps 1–5) and `slide006_core137` (Map4)
  have no image and are ignored. *Why:* there is no image to tile, and overlap tests could not match the Map4 orphan to any core.
  The remaining 1171 maps match the count in Foucart et al. (2021).
- **A0.4 Map folder k = pathologist k** on every image. *Why:* stable per-folder signatures across all 6 slides
  (Phase 0 report §5). This is not provable from the files.
- **A0.5 Label semantics.** Resolved by user decisions D1 and D2 below.
- **A0.6 All-zero masks.** Resolved by user decision D3 below.

## Patch dataset (Phase 1): user decisions (2026-10-20)
- **D1 Value 0 = unannotated (no opinion), not benign.** A reader's patch label is their dominant class over the
  patch's tissue pixels, with 0 counted as its own class. The label is valid only if that class covers >= 60%
  (`min_coverage`) and is not 0. Otherwise the reader gives no label ("none").
- **D2 Value 6 = benign**, merged with value 1.
- **D3 Entirely-zero masks = reader did not annotate that core.** The 20 masks are excluded, and coverage is recomputed:
  cores per reader r1 241, r2 139, r3 232, r4 238, r5 237, r6 64; readers per core: >=3 243, >=4 232, >=5 152, 6 36.
  One core (slide005_core102: Maps 3 and 5 empty) is left with 2 readers, so it yields no kept patches.
- **D4 Binary task: G3 -> 0, G4 or G5 -> 1.** Benign readers are handled by `benign_rule`: `ignore` (reader -> NA, default
  for now) or `drop` (drop the patch). Both are reported; the final choice is pending.
- **D5 Splits: 3 folds grouped by slide, each with 2 test slides.** There is no core-level split, because patient IDs
  are unavailable. Validation comes from training slides. The 10% labelled subset comes from training slides only,
  stratified, with a fixed seed.
- **D6 Both 512 px and 1024 px tiles** are built (each resized to 224x224). No choice has been made yet.
- **D7 Map2 kept.** Any reader can be excluded with `exclude_readers` (e.g. `exclude_readers=[2]`).
- **D8 Agreement statistics use tissue pixels only, with value 0 excluded.**

## Patch dataset (Phase 1): implementation choices
- **A1.1 Tissue mask.** HSV saturation > Otsu threshold, computed per core on an 8x-downsampled saturation image.
  No morphology. Thresholds range 58–83 (median 69). *Why:* the task asks for a simple Otsu/saturation mask.
  Visual check: lumens and glass are excluded, stroma and epithelium kept.
- **A1.2 Tiling grid.** Non-overlapping tiles on a grid centred in the image. Incomplete edge tiles are dropped.
  Image sides are multiples of 512, so 512 px tiling is exact. For 1024 px, a 4608 or 5632 px side leaves a
  256 px margin on each side, which is glass. Tiles with < 50% tissue are skipped.
- **A1.3 Patch images.** Crops are resized to 224x224 with LANCZOS and saved as lossless PNG. *Why:* avoids a second
  round of JPEG compression.
  Every tissue tile is saved, not only kept patches, so labelling rules can change without re-tiling.
- **A1.4 Coverage denominator = all tissue pixels in the patch**, including unannotated ones (follows D1).
- **A1.5 Column meanings.** `n_readers` = number of valid binary votes. `n_annotators` = readers who annotated the core
  and are not excluded. `q = votes_g4 / n_readers`. `tie` means votes_g4 = n_readers / 2. A tie has no
  `majority_label`. `raw_r{k}` and `cov_r{k}` keep each reader's raw label and coverage for later
  vote-handling modes (linked / permuted / counts_only).
- **A1.6 Fold pairing.** Test pairs {001,003}, {002,005}, {006,007}. Chosen out of all 15 partitions by minimising
  sum|test share - 1/3| + sum|test G4 rate - overall|. The same partition ranks first for all four tile/rule
  combinations, so the pairing is fixed in the config.
- **A1.7 Validation split.** About 15% of training-slide patches, grouped by core (StratifiedGroupKFold, 7 splits,
  first split, stratified by majority label with ties as a third stratum). Val cores may share a patient with
  train cores because patient IDs are unknown. This affects only model selection.
- **A1.8 Labelled subset.** Round(10%) of each stratum (G3 / G4 / tie) of the train split, using rng([seed, fold]),
  seed 0. Tie patches can be drawn as labelled but are excluded from majority-label training (`train_majority = 0`),
  so the unlabelled pool stays independent of ties. The labelled subset stays fixed across model seeds.
  Stratifying uses the majority labels of all train patches, including ones that end up unlabelled. This is a
  dataset-construction step requested in the task; it never enters a loss.
- **A1.9 Leakage-safe file layout.** `train_unlabelled.csv`, `val.csv` and `test.csv` carry only ids and paths. Votes exist
  only in `patches.csv` (analysis and evaluation) and `labelled_list.csv` (training).
- **A1.10 Unlabelled pool definition [pending].** By default the unlabelled pool is the kept patches: those with >= 3 valid
  G3/G4-5 votes. That filter uses votes on unlabelled patches to decide which images enter Stage III, which
  arguably is a sampling decision covered by the leakage rule. An alternative pool, "all tissue tiles on train
  cores", needs no votes (fold0: 6406 vs 4622 tiles at 512 px). It is reported but not yet used.

## Phase 1 approval: user decisions (2026-10-20)
- **D9 Main setting = p512 tiles.** p1024 is kept only for a later sensitivity check.
- **D10 Label set = `labels_benign-drop`.** A patch is dropped if any reader's valid label is benign.
- **D11 Stage III unlabelled pool = the vote-filtered `train_unlabelled` split**, the same for every method. This defines
  the task as *grading cancer patches* (G3 vs G4/5). Selecting the pool uses annotation information: patches enter
  only if >= 3 readers gave a valid G3/G4/5 label. That information never enters a loss, but it does decide which
  images Stage III may pseudo-label. The vote-free pool ("all tissue tiles on training cores") remains as a
  robustness option: `data.unlabelled_pool=all_tissue`.
- **D12 Reader exclusion.** `data.exclude_readers` in the training config selects a label set built with that reader
  removed. Built: `excl-r1`, `excl-r2`, `excl-r1-r2` (p512, benign-drop). Excluding a reader changes which patches
  are kept and their majority labels, so exclusion happens when the label set is built, not at training time.
  Kept patches: all readers 8,897; no r1 7,212 (82% unanimous); no r2 8,806; no r1+r2 6,940.
  The fold pairing stays fixed across these sets.

## HSRL implementation (Phase 2)
Values fixed by the paper/task: EfficientNet-B2 (ImageNet), 128-d L2-normalised projection, squared Euclidean distance,
Eq. 5 with alpha=1.0, beta=0.5, gamma=0.5; Stage I AdamW lr 1e-4, wd 1e-4, 30 epochs; Stage II lr 1e-3, 5 epochs;
Stage III tau=0.85, 10 epochs, lr 1e-5; flips, 180-degree rotation, colour jitter; 224x224 input.
- **A2.1 Backbone.** timm `efficientnet_b2` (default pretrained tag `ra_in1k`), `num_classes=0`, global average pooling,
  1408-d features, `drop_rate=0`, `drop_path_rate=0`. *Why:* the paper gives no dropout; this keeps the backbone deterministic.
- **A2.2 Projection head g.** Linear(1408, 1408) -> ReLU -> Linear(1408, 128) -> L2-normalise. *Why:* the hidden width is unspecified.
  With width 1408, f is 7.70M params and f+g is 9.86M, matching the paper's Table 3 (baseline 7.7M, HSRL 9.9M).
- **A2.3 Classifier h.** Linear(1408, 2) on backbone features; softmax in the loss and at prediction.
- **A2.4 Augmentation.** H-flip p=0.5, V-flip p=0.5, rotation by exactly 180 degrees with p=0.5 (the paper's
  "180° rotations", read literally; note that H+V flip together already equal a 180-degree rotation), and ColorJitter(brightness 0.2,
  contrast 0.2, saturation 0.2, hue 0.05). The jitter strengths are unspecified. ImageNet mean/std normalisation. Applied
  in every training stage, including Stage II, since the paper says "during training". No augmentation at prediction.
  Alternatives available: `augment.rotation=rot90|none`.
- **A2.5 Tuple mining (not in the paper; task default).** Class-balanced batches of 32 (16 per class). Every sample in
  the batch is an anchor. p = random same-class sample; n = nearest different-class sample; c = second-nearest
  different-class sample (`conf_rule=second_nearest`). Option (ii) `boundary` picks the different-class sample, other than n,
  with the smallest |d(x, own centroid) - d(x, nearest other centroid)|. Centroids are means of the
  normalised batch embeddings, not renormalised. Mining uses detached embeddings; the loss uses the same forward pass's
  embeddings with gradient. In a binary task n and c always share a class.
- **A2.6 Loss reduction.** Mean over all anchors in the batch. The hinge terms are summed unweighted, as in Eq. 5.
  `stage1.terms=[1,3]` drops the beta term.
- **A2.7 Class-balanced sampler.** Each class is drawn without replacement from a reshuffled permutation, refilled when
  exhausted, so the minority class (G3) is cycled more often. One epoch = ceil(N_labelled / 32) batches.
- **A2.8 Batch size 32 in all stages.** The paper does not give one. Fits easily in 8 GB with bf16 autocast (see smoke-test memory).
- **A2.9 Optimisers.** AdamW with wd 1e-4 in all stages. The paper names AdamW only for Stage I. Constant learning rate,
  no warm-up or schedule (none given).
- **A2.10 Stage II.** f and g are frozen and f runs in eval mode, so BatchNorm statistics are not updated ("frozen").
  Labelled loader shuffled (not class-balanced). Targets: `hard` (one-hot majority) or `soft` (1-q, q).
- **A2.11 Stage III.** One prediction pass over the unlabelled pool (no augmentation, eval mode); accept max prob > tau
  with hard argmax pseudo-labels. Then train f, g, h on labelled + accepted data with CE, shuffled, model in train mode.
  g gets no gradient, since only CE is used. Labelled targets are hard by default (`stage3.labelled_targets`). With
  `refresh_every_epoch=true`, pseudo-labels are re-predicted before each epoch.
- **A2.12 Model selection.** No early stopping or checkpoint selection: the model after the last epoch of each stage is
  used, since the paper describes none. Val predictions are saved for reporting only.
- **A2.13 Mixed precision.** bf16 autocast for the backbone; embeddings, distances, logits and losses in fp32; no grad scaler.
- **A2.14 Tuple logging.** Every Stage I tuple → `tuples_stage1.csv`: epoch, global step, the four patch_ids,
  d_ap / d_an / d_nc / d_ac (computed in the forward pass before that step's update), the three hinge values, and
  `t{k}_active` = hinge > 0. All three hinges are logged even when a term is excluded from the loss.
- **A2.15 Supervised-only baseline.** f + h trained end-to-end with CE on the labelled set. The schedule (35 epochs = the
  Stage I + II epoch budget, lr 1e-4) is provisional until Phase 3.
- **A2.16 Determinism.** Seeds for python/numpy/torch, `cudnn.deterministic=True`, seeded DataLoader generators per stage,
  and a seeded sampler/mining RNG. Bit-exact GPU reproducibility is not guaranteed.
- **A2.17 Leakage enforcement in code.** `SplitData.labelled` is the only table with labels or votes. Unlabelled, val and
  test tables carry ids and paths only. Hidden labels are reached only through `SplitData.eval_labels`. It is called by
  evaluation code after each stage, and by the Stage I collapse monitor, which scores kNN on val (see D14). The monitor
  passes nothing back into training. Unit test: `test_gleason_split_has_votes_only_on_labelled`.

## Phase 2 approval: user decisions (2026-10-20)
- **D13 Augmentation:** random rot90 (0/90/180/270, uniform) replaces the fixed 180° rotation; H/V flips kept
  (`augment.rotation=rot90`, now the default). This supersedes the rotation part of A2.4.
- **D14 Collapse monitoring in Stage I**, before training (epoch -1) and after every epoch, written to `stage1_monitor.csv`:
  - From the tuples mined during the epoch: mean d_ap, d_an, d_nc, d_ac and the fraction of tuples where each term is active.
  - Embedding spread = mean pairwise squared distance between projection embeddings z of a fixed val subset
    (512 patches, seed 0, eval mode, no augmentation). Also logged: `val_mean_norm_of_mean`, the norm of the mean
    embedding (→ 1 when all z coincide).
  - kNN (k=5) accuracy and balanced accuracy on that val subset, using z, with the labelled training set as reference
    (squared Euclidean, majority of 5). Val ties are excluded from scoring.
  - If embeddings collapse, it is reported; hyperparameters are not changed to hide it.
- **D15 tau stays 0.85.** Stage III pseudo-label coverage and precision (overall, unanimous, split-vote) are reported.
  Coverage below 5% raises a flag in `metrics.json`; tau is not changed.
- **D16 Ablation "HSRL without Stage I"** (paper Table 4): `stage1.enabled=false`. Stage II trains h with CE on frozen
  ImageNet features (5 epochs, lr 1e-3), then the same Stage III.
- **D17 Supervised-only schedule confirmed:** 35 epochs, lr 1e-4, AdamW wd 1e-4, batch 32, CE on the labelled set
  (A2.15 is no longer provisional).

## Tuple census (Phase 4)
No `mhist_tuple_census.py` was provided, so the census is written from scratch (`analysis/tuple_census.py`).
- **A4.1 Labelled set** = the Stage I training set (fold's `labelled_list.csv`, `train_majority == 1`), linked votes.
- **A4.2 Tuple set A.** 100k tuples sampled uniformly with HSRL's role constraints: a uniform; p uniform over the same
  majority class, p != a; n and c uniform over the other class, n != c. Seed 0.
- **A4.3 Tuple set B.** All tuples mined in one Stage I epoch, read from `tuples_stage1.csv` (512 per epoch = 16 batches x 32).
  Epochs 0 and 29 are both reported.
- **A4.4 Linked verdict.** An ordering s_x > s_y is evaluated only if both pairs have >= 3 shared readers; otherwise it is
  "skipped" (counts reported). s_x and s_y may come from different shared-reader subsets. Equal values are a tie
  (|diff| <= 1e-9). Counts-only bounds use the patch's own q.
- **A4.5 Bridging pseudo-labels to tuples.** Pseudo-labels are on unlabelled patches, which never appear in tuples. Each
  labelled patch gets a violation rate: the fraction of its term-verdicts that are linked-violated, over all logged
  Stage I tuples and all roles. It also gets an undecided rate (counts-only). An accepted pseudo-labelled patch inherits
  the mean rate of its k=5 nearest labelled patches in the final Stage I embedding (`model_stage1.pt`, z, eval mode).
  The rate's AUROC for "wrong" (pseudo != hidden majority, ties excluded) is tested by permutation (2000).
  Also reported: within unanimous and within split-vote patches, and at core level (Spearman over cores with >= 5
  accepted patches).
- **A4.6 Statistical unit caveat.** Permutation p-values treat patches as independent. Patches within a core are
  correlated, so these p-values are optimistic; the core-level correlation is the more honest unit. Slide-level
  inference needs the other folds.

## Fold-0 approval: user decisions (2026-10-20)
- **D18 Main grid.** 4 configs × 5 seeds (0–4) × 3 folds, same monitoring, saved in `results/main/f{fold}s{seed}_{config}`.
  The fold-0 seed-0 runs from the previous round were moved there and reused: same code and config.
  Seeds change model-head initialisation, sampling, augmentation and mining. The labelled subset per fold is fixed (A1.8).
- **D19 Deviation experiments (NOT the paper's protocol)**, fold 0, seeds 0–2, in `results/deviations/`:
  `hsrl_s1e60` (Stage I 60 epochs), `hsrl_no_t2_s1e60` (matching control), `hsrl_boundary` (conf_rule=boundary, 30 epochs).
- **D20 Census** on HSRL original for all folds. It runs for every seed (15 runs), so seed variability is visible. Core level
  is primary for the pseudo-label analysis; patch level is secondary.
- **D21 No new losses.**

## Aggregation and plots
- **A3.1 Runs as units.** mean ± std (ddof=1) over all (fold, seed) runs. Paired differences use matching (fold, seed).
  The 95% t-interval over 15 pairs treats them as independent, which they are not (only 3 test-slide sets), so
  per-fold mean differences and the number of folds that agree in sign are reported as the conservative view.
- **A3.2 "Before Stage III"** = the model after Stage II (Stage I + classifier warm-up) for HSRL variants. Supervised-only
  has a single stage.
- **A3.3 Collapse and escape (Stage I monitor).** With s0 the val embedding spread before training: collapse epoch = first
  epoch with spread < 0.1·s0; escape epoch = first later epoch with spread > 0.5·s0.
- **A3.4 Core-level census statistics.** Spearman over cores with >= 5 accepted non-tie pseudo-labels, between the core's
  pseudo-label error rate and the mean violation (or counts-undecided) rate of its labelled patches. Also reported: a
  partial Spearman controlling for the core's split-vote share among accepted patches (rank residualisation), with
  two-sided permutation p-values over cores (5000).
- **A3.5 t-SNE** (fold 0, seed 0, test patches): PCA to 50 dims, then t-SNE (perplexity 30, PCA init, seed 0). Row 1 shows
  backbone features f of each config's final model, comparable across configs and what the classifier uses. Row 2 shows
  projection z (the paper's choice) after Stage I and at the end of training, for the two HSRL variants that train g.
  Silhouette (cosine, majority labels, ties excluded) is computed in the original space, not on the t-SNE map.
- **A3.6 Resumable queue** (`scripts/run_queue.py`). A run is done when its `metrics.json` exists. Incomplete run
  directories are re-run from scratch. `results/STOP` pauses the queue after the current job.
- **A3.7 Rise epoch (REPORT.md §2).** First epoch after the spread minimum at which spread > 0.5·s0, with no collapse
  threshold. Added because 5 fold-2 runs without term 2 bottom out at 0.13·s0, above the 0.1·s0 threshold of A3.3, and so
  get no escape epoch there although their curves have the same shape.

## Batch 2: user decisions (2026-10-21), all DEVIATIONS from the paper's protocol
- **D22 60-epoch Stage I on all folds.** `hsrl_s1e60` and `hsrl_no_t2_s1e60` (Stage I 60 epochs, everything else as the paper),
  5 seeds × 3 folds, in `results/deviations/`. Fold-0 seeds 0–2 come from the earlier deviation runs (same code and config);
  seeds 3–4 and folds 1–2 are new.
- **D23 Budget-matched supervised control** `supervised_e65`: supervised-only, 65 epochs (60 Stage I + 5 Stage II), lr 1e-4,
  otherwise as D17. 5 seeds × 3 folds. Stage III's 10 epochs are not added to the budget, as instructed.
- **D24 Census** on all 15 `hsrl_s1e60` runs, using mined tuples from epochs 0, 29 and 59 (`results/census_summary_s1e60/`).
- No FixMatch-type baseline and no new losses.

## Batch 3: user decisions (2026-10-22)
- **D25 Soft-label baselines**, 5 seeds × 3 folds each, in `results/soft/`:
  - `supervised_soft` / `supervised_soft_e65`: Peterson-style supervised-only with soft targets (1−q, q), 35 / 65 epochs, no
    structural training.
  - `hsrl_soft` / `hsrl_soft_s1e60`: HSRL with soft Stage II targets and majority-label tuples, Stage I 30 / 60 epochs.
    Stage III is unchanged: hard majority targets on labelled patches plus hard pseudo-labels.
  Soft targets use the votes of labelled training patches only (leakage rule unchanged).
- **D26 Pseudo-label precision at equal coverage and coverage at equal precision**, computed from the saved Stage III files of
  all runs. No retraining.
- **D27 Not now:** interval loss and changes to tuple sampling. Decisions on term 2, fixed tuple sampling and the Stage I
  schedule come from the supervisor.

## Soft targets and pseudo-label coverage (batch 3)
- **A5.1 Same labelled set as the hard-target runs.** `include_ties=false`, so tie patches stay out of the labelled training
  set, and q is never 0.5 there. *Why:* soft and hard runs then train on identical images and differ only in the target,
  which keeps the paired comparison clean. Including ties would be a separate, later choice.
- **A5.2 q = votes_g4 / n_readers** over the patch's valid binary votes, linked readers, from `labelled_list.csv`. Soft
  cross-entropy = −Σ_k t_k log p_k.
- **A5.3 Stage I reuse.** Each `hsrl_soft*` run loads the Stage I checkpoint of the hard-target run with the same fold, seed
  and Stage I schedule (`stage1.reuse_from`), and copies its monitor file. Stage I never sees Stage II/III settings, and
  training is deterministic. The loader refuses a source whose seed, model, augmentation, data or Stage I settings differ.
  Check: re-running `f2s4_hsrl` from its own checkpoint reproduced every Stage II/III prediction exactly (max |Δp| = 0).
  This saves about 2.5 h and makes Stage I identical between the soft and hard runs.
- **A5.4 Precision/coverage curves.** The unlabelled pool (identical across configs within a fold) is ranked by the Stage II
  model's p_max; ties are broken by patch_id. Coverage = top-k / pool size, with tie patches counted in the pool, as in the
  Stage III diagnostics. Precision = correct / non-tie among the top-k, against hidden majority labels (evaluation only).
  Coverage at precision p = the largest top-k fraction with precision >= p, with k >= 50 to avoid tiny-k noise. Levels:
  coverage 0.3, 0.5, 0.7, 0.8; precision 0.90, 0.93, 0.95. Supervised-only runs have no Stage III file and are not included.

## Batch 4: user decisions (2026-10-22): test of the Map1-bias explanation (REPORT §6.3)
- **D28 Map1-excluded runs** with the pre-built label set `labels_benign-drop_excl-r1` (`data.exclude_readers=[1]`), 5 seeds ×
  3 folds, in `results/excl_r1/`: supervised hard and soft (35 epochs); HSRL hard and soft Stage II (Stage I 30 epochs).
  Each soft HSRL run reuses the Stage I of the hard HSRL run with the same fold, seed and label set (A5.3).
- **D29 Within-setting comparison only.** Excluding Map1 changes which patches are kept (7,212 vs 8,897), their majority
  labels, ties, and the labelled subset (386–420 vs 470–509 used per fold). So soft vs hard is compared only within the
  Map1-excluded setting, paired on fold and seed. Against the with-Map1 runs, only the size of the soft − hard
  difference is compared, never raw metrics.
- **D30** No other runs and no new losses.
- **A6.1 Fixed across settings:** fold pairing, split procedure and seeds. The labelled subset, val and test splits are
  redrawn by the same procedure on the Map1-excluded kept patches (A1.7–A1.8), because the kept-patch set differs.

## EXPLORATORY PILOT: interval losses on frozen features (user decisions 2026-10-25; recorded before the full run)
- **D31 Scope.** The frozen-feature pilot of the supervisor's pairwise interval loss is allowed (`hsrl/pilot_frozen.py`,
  `configs/pilot_frozen.yaml`, `results/pilot_frozen/`). Integrating any proposed loss into full HSRL still needs the
  user's go-ahead.
- **D32 Features.** ImageNet EfficientNet-B2 (timm `ra_in1k`), global-pooled 1408-d features of every kept patch, eval
  mode, no augmentation, extracted once and cached. No HSRL-trained backbone, so the Stage I collapse cannot confound
  the pilot.
- **D33 Methods.**
  - Interval loss and independent worst-case loss (A7.2), each in vote modes linked, permuted and counts_only.
  - Baselines on the same features: linear probe with hard targets; linear probe with soft targets (1 − q, q); a head
    trained with HSRL terms 1 + 3; an annotator-aware classifier.
- **D34 Fixed sampling.** One set of tuples per (fold, seed), shared by every loss.
- **D35 Pre-registered success criterion.** A method succeeds if, against the best baseline, it gains at least +1 point
  in balanced accuracy or split-vote accuracy in at least 12 of 15 pairs, AND the fold-mean gain is at least +1 point
  on at least 2 of 3 folds. "Linkage matters" = linked beats permuted by the same standard.
  - Best baseline = the baseline with the highest mean over the 15 runs, chosen per metric.
  - Implementation: a pair counts only if its own difference is at least +0.010, and a fold counts only if its mean
    difference over the 5 seeds is at least +0.010.
- **A7.1 Which "two variants".** Read as the plan's two pair-based losses on the agreement interval [L, U], with
  similarity t = 1 − d/4 on L2-normalised embeddings:
  - interval (feasibility) loss: max(0, L − t)² + max(0, t − U)², from plan §3;
  - independent worst-case loss: max over s in [L, U] of s(t − 1)² + (1 − s)t², from plan §4.
- **A7.2 Pair targets per vote mode.**
  - counts_only: L, U = Fréchet bounds from q.
  - linked: pairs with at least 3 shared readers get L = U = observed agreement; others fall back to the counts-only
    bounds. This is 88% exact on fold 0.
  - permuted: as linked, after reassigning votes among each patch's observed readers (seed 1000·fold + seed). This
    keeps q, so the fallback pairs are identical to linked.
- **A7.3 Tuples.** 20 per labelled anchor: p from the same majority class, n ≠ c from the other class, drawn uniformly
  (no hard mining). Pair losses train on the four pairs of each tuple (ap, an, nc, ac). HSRL terms 1 + 3 use the tuples
  directly (α = 1, γ = 0.5).
- **A7.4 Fixed hyperparameters, chosen before any result and not tuned on validation or test.**
  - Head: Linear(1408, 512) → ReLU → Linear(512, 128) → L2-normalise. AdamW, lr 1e-3, wd 1e-4, 50 epochs over the
    fixed tuples, 256 tuples per step.
  - Features standardised with labelled-training mean and std.
  - Linear probes: full batch, AdamW, lr 1e-2, wd 1e-4, 500 steps.
  - Annotator-aware classifier: Linear(1408, 128) + ReLU, then one 2-way head per reader, trained on every observed
    (patch, reader) label (AdamW, lr 1e-3, 1000 steps). Prediction = mean of the six readers' probabilities.
  - Initialisation seeds are shared across methods within a (fold, seed); mini-batch order is identical.
- **A7.5 Evaluation.**
  - Primary: a hard-target linear probe on each head's embedding, scored on test non-tie patches (balanced accuracy,
    split-vote accuracy, unanimous accuracy, Brier).
  - Secondary: a soft-target probe on the same embedding; reader-agreement retrieval = Spearman correlation of t with
    linked agreement on 20,000 random test pairs with at least 3 shared readers (hidden test votes, evaluation only).
- **A7.6 Smoke run.** Fold 0, seed 0 was run once to time the pipeline and check training. No setting was changed after
  seeing its numbers.

## Overnight batch (user decisions 2026-10-25)
- **D36 Pilot robustness (secondary, frozen features; `configs/pilot_frozen_robust.yaml`).**
  - Repeated permutations: 5 draws (seeds 1000·fold + seed + 100000·k; draw 0 = the main pilot's draw, reproduced
    exactly).
  - Consistent reader renaming: one fixed relabelling of reader IDs for the whole dataset. It must leave linked
    results unchanged (verified at 0.000 on the smoke run).
  - The full pilot again with Map1 excluded (`results/pilot_frozen_excl_r1/`, its own feature cache, because the kept
    patch set differs).
  - The pre-registered criterion (D35) applies only to the main pilot.
- **D37 Reader-swap control for §8.** Soft vs hard with Map4 excluded (`labels_benign-drop_excl-r4`: 7,471 patches,
  against 7,212 without Map1). Map4 has similar coverage and no grading bias (Phase 0/1). Same 4 configs and Stage I
  reuse as batch 4. The soft − hard shift is compared within each setting (with Map1 / Map1 excluded / Map4 excluded)
  in `results/reader_swap_summary/`.
- **D38 Tile-size sensitivity (D9).** The 4 main configurations on 1024 px tiles (`labels_benign-drop`), 5 seeds × 3
  folds, same settings as the 512 px grid, in `results/p1024/`. About 120 labelled patches per fold.

## MHIST (user permission to train, 2026-10-31)
- **D39 MHIST runs allowed.** Raw data in `data/mhist/` (annotations.csv + images/), verified:
  3,152 PNGs at 224x224 RGB; columns Image Name, Majority Vote Label (HP / SSA), Number of Annotators who Selected
  SSA (Out of 7), Partition. Official split: 2,175 train / 977 test. HP 2,162 / SSA 990. The majority label matches
  "SSA votes ≥ 4" for every image. No patient or slide IDs are released.
- **A8.1 Label set** (`data/mhist_prepare.py`, `data/processed/mhist/labels_p10` and `labels_p100`).
  - SSA = label 1. q = SSA votes / 7, counts only; reader columns stay empty, so only counts-only vote handling is
    possible.
  - There are no ties (7 readers). "Unanimous" = 0 or 7 SSA votes (34% of images; 33% of the test set).
- **A8.2 Draws instead of folds.** The paper uses the official split, so there are no slide folds. Each "fold" k is an
  independent draw on the official train partition, with seed k:
  - validation = 10% of train (218 images), stratified;
  - labelled = 10% of train (218 images, 63 of them SSA), stratified, from the non-validation images;
  - unlabelled pool = the remaining 1,739 train images (no vote-based filtering, unlike Gleason);
  - test = the official 977 images.
  The 100% reference (`labels_p100`) labels all 1,957 non-validation train images. The paper averages 3 runs; we use
  5 draws, run k with seed k.
- **A8.3 Hyperparameters** are unchanged from the Gleason/paper settings. Images are already 224 px, as in the paper's
  MHIST setting. Augmentation as D13.
- **A8.4 Paper ablation "w/o HSRL (Triplet Loss)".** Removing the ambiguity-aware negative x_c and its margin γ removes
  both terms that involve c, leaving HSRL term 1 only (`stage1.terms=[1]`, a hard-negative triplet loss).
- **A8.5 Metrics.** Macro precision is now also reported, because the paper reports accuracy and macro P/R/F1. Macro
  recall = balanced accuracy.
- **A8.6 Label curve for supervised training** (`labels_p20`, `labels_p50`: 435 and 1,088 labelled images).
  - Same validation set per draw as at 10% and 100%: the validation draw comes first from the same seed.
  - The labelled sets are separate stratified draws, not nested (the 20% set does not contain the 10% set). Nesting is
    not needed for a learning curve averaged over 5 draws.
  - Supervised schedule unchanged (35 epochs) at every fraction, as for the 100% reference.
- **A8.7 Soft targets on MHIST** (`supervised_soft`, `hsrl_soft`): (1 − q, q) with q = SSA votes / 7, for the
  labelled images only, as in Batch 3 on Gleason (D25). `hsrl_soft` reuses the Stage I checkpoint of the hard-target
  `hsrl` run with the same draw. The reuse check now also compares `data.labelled_pct`.
- **A8.8 Census on MHIST is counts-only.** No reader identities, so every linked verdict is "skipped". Every MHIST
  image was read by the same 7 pathologists, so the counts-only bounds L = |q_i + q_j − 1|, U = 1 − |q_i − q_j| are
  exact bounds on pairwise agreement here, not an approximation as on Gleason. There are no cores (core_id = image), so
  the core-level pseudo-label analysis does not apply. The patch-level analysis uses the counts-undecided rate of the
  5 nearest labelled images.
- **D40 MHIST frozen-feature pilot, counts only (EXPLORATORY; allowed 2026-10-31).** `configs/pilot_frozen_mhist.yaml`.
  Same design and hyperparameters as the Gleason pilot (§9), fixed before running:
  - Methods: probe_hard, probe_soft, hsrl_t13 (baselines); interval_counts_only, worstcase_counts_only. No linked,
    permuted or annotator-aware methods: MHIST has no reader identities.
  - 5 labelled draws × 3 seeds = 15 pairs.
  - Success criterion: ≥ +1 point on balanced or split-vote accuracy over the best baseline in ≥ 12/15 pairs and on
    ≥ 4/5 draws (Gleason: ≥ 2/3 folds; 4/5 keeps the bar at least as strict).
  - Unlike Gleason, the interval [L, U] from vote counts is exact here (same 7 readers on every image, A8.8).
- **D41 MHIST protocol checks for the 10% gap (diagnostics, allowed 2026-10-31).** Results in `results/mhist_protocol/`,
  5 draws each; everything else as in Batch 6.
  - Best epoch on test: `eval.per_epoch_test=true` logs val and test metrics after every epoch (`epoch_eval.csv`).
    It is never used for training or selection. It measures how much choosing the epoch on the test set would add.
    Runs: supervised, and HSRL with the Batch 6 Stage I reused (Stage II and III epochs logged).
  - Input size 288 px: `augment.resize=288` (EfficientNet-B2's pretrained test size; MHIST images are 224 px, so this
    upsamples). Supervised and full HSRL (Stage I retrained).
  - Labelled set = 10% of all 3,152 images (315 labelled, `labels_p10all`) instead of 10% of train (218). Same
    validation set. Supervised and full HSRL.
- **D42 MHIST pilot on fine-tuned features (EXPLORATORY; user go-ahead 2026-10-31; recorded before running).**
  `configs/pilot_ft_mhist.yaml`, results in `results/pilot_ft_mhist/`. It tests whether the D40 gain survives better
  features.
  - Features: draw k uses the backbone f of `results/mhist/f{k}s{k}_supervised/model_final.pt`. That run is end-to-end
    CE for 35 epochs on draw k's 218 labelled images (hard targets, official split). Features are the 1408-d pooled
    output in eval mode, with no augmentation and bf16, for all 3,152 images. They are cached per draw
    (`data/processed/mhist/features_effb2_ft_supervised_draw{k}.npz`).
  - Leakage guard (`check_backbone_source`): the run must be finished, supervised, MHIST, the same draw and the same
    labelled set. The only labels the backbone has seen are those of the pilot's own labelled images.
  - Everything else is inherited unchanged from D40: methods, head, probe, tuples, seeds, and the criterion (≥ +1 point
    on balanced or split-vote accuracy over the best baseline in ≥ 12/15 pairs and ≥ 4/5 draws).
  - Known caveat: the backbone was fit to the labelled images, so their features separate more cleanly than test
    features. This affects every method equally. Sanity anchor: `probe_hard` should land near the supervised model's
    own test accuracy (76.7%).
  - Reading, fixed now: if `interval_counts_only` meets the criterion, the frozen-feature gain holds on fine-tuned
    features, which supports a full-HSRL test (that test still needs the user's go-ahead). If it does not, the D40 gain
    is specific to ImageNet features. Either outcome is reported.
- **D43 MHIST random-split check for the 10% gap (diagnostic; user go-ahead 2026-10-31; recorded before running).**
  `data/mhist_prepare.py --split random` → `labels_p10rs`, `labels_p100rs`; runs in `results/mhist_randsplit/`.
  - Per draw k, a random image-level test set of 977 images (the official size) is drawn from all 3,152 images,
    stratified by majority label (670 HP, 307 SSA; 31.4% SSA, against 36.8% in the official test set). RNG
    [20261031, k, 1]. The other 2,175 images are train. Validation (218) and labelled (218) sets are then drawn from
    them exactly as in A8.2.
  - Stratified, because the paper does not say how a non-official split would be made, and stratification is the
    common default.
  - Runs, 5 draws: supervised 10%, HSRL 10%, HSRL without Stage I 10%, and supervised 100% (1,957 labelled). Batch 6
    settings otherwise.
  - Caveats: MHIST has no patient or slide IDs, so a random image split can put images of one patient or polyp on both
    sides. The paper does not say whether its split avoids that. Test sets differ per draw and from the official one,
    so comparisons with `results/mhist` are of means, not paired.
  - Reading, fixed now: the random-split explanation predicts that every configuration rises by about 3–4 points. It
    only explains the paper's numbers if the paper's pattern also appears: supervised 100% near 86.0, and HSRL 10% near
    86.2 and well above supervised 10%. If HSRL 10% stays about level with supervised 10% here too, a random split
    explains part of the absolute gap but not the paper's HSRL advantage.
- **D44 Step 1 of the extension plan: does the joint four-image loss differ from the pairwise worst case? (analysis
  only, no training; written 2026-11-01, before the full run.)** `analysis/joint_check.py`, results in
  `results/joint_check/`.
  - Question: plan §4's joint loss only differs from its matched independent baseline (each pair's worst case taken
    alone, plan §4 last part) when the six pairwise worst cases cannot hold together. If that almost never happens on
    real tuples, the joint loss reduces to the independent one, and building it would add nothing on these data.
  - Embeddings: end of Stage I of the existing HSRL runs (`model_stage1.pt`; 5 MHIST draws, 15 Gleason fold × seed
    runs). t_ij = 1 − d_ij / 4 as in the plan. Caveat: these are embeddings trained with majority-label tuples. A
    network trained with the joint loss would end in a different geometry; this measures the starting situation.
  - Tuples: those HSRL mined in the last Stage I epoch (fixed tuple sampling, plan §5), plus 1,000 random role-valid
    tuples per run. An embedding-free scope measure (how many of the 2^m pairwise worst cases are jointly feasible) on
    200 tuples per set.
  - Allocation models: MHIST exact (integer, 7 readers, solved by MILP) and the LP relaxation; Gleason relaxation only.
    On Gleason the readers differ between cores, so the relaxation is a common-population model there, not a
    guaranteed bound (plan §2).
  - Votes: labelled training images only (the tuple members are checked against the labelled list).
  - Reading, fixed in the script before any data were seen: primary = MHIST, mined tuples, exact counts, mean over the
    5 draws. The joint loss has something to act on if the joint worst case is below the independent one in ≥ 10% of
    tuples AND those gaps average ≥ 5% of the loss. Thresholds are a judgement: below 1 tuple in 10, the joint loss
    would behave like the independent one almost everywhere, and a training effect would be hard to detect with 5
    draws. Gleason is reported alongside as secondary (model caveat above).
  - Disclosure: a smoke test on MHIST draw 0 (with a smaller random set) was run after the criterion was written and
    showed 12.9% of mined tuples with a gap, averaging 6.9% of the loss. The thresholds were not changed after that.
  - If met: building the joint loss is justified (still needs the user's go-ahead). If not: step 2 starts
    with supported ordering and the interval loss, and the joint loss is set aside for these datasets.
- **D45 Extension plan step 2: annotation-aware Stage I losses inside full HSRL (user go-ahead 2026-11-01; recorded
  before running).** Batches 10 (`results/mhist_ext/`) and 11 (`results/gleason_ext/`); losses in `hsrl/losses.py`,
  vote plumbing in `hsrl/stages.py` (`labelled_votes`, `tuple_votes`).
  - What changes (plan §5): only Stage I's structural loss. Backbone, head, tuple mining (HSRL's: majority labels +
    embedding hardness, fixed sampling), schedule (30 epochs, lr 1e-4), Stage II with soft targets (1 − q, q), and
    Stage III (τ = 0.85, hard labelled targets) stay as in the matched baseline `hsrl_soft` (Batch 7 on MHIST,
    Batch 3 on Gleason). Nothing is tuned.
  - `supported` (plan §3): HSRL's three hinges, each kept only when the votes guarantee its ordering (L_x > U_y + 1e-6;
    term 1: s_ap > s_an, term 2: s_ap > s_nc, term 3: s_ap > s_ac, as in the census). Undecided and contradicted
    orderings are dropped, not reversed. Margins stay α/β/γ and the mean is over tuples, so a kept hinge has exactly
    HSRL's gradient (selection only; turning the guaranteed gap into a margin is left for a sensitivity study).
    Term 2 choice the plan asks us to state: term 2 is read as the ordering s_ap > s_nc and filtered like the others;
    it is not kept as a separate regulariser.
  - Matched controls (plan §7, "match the number of selected tuples"): `supported_random` keeps the same number of
    hinges per term and batch at random; `supported_conf` keeps the same number from the tuples whose term images
    have the most extreme votes (mean |2q − 1|; ordinary confidence filtering). Own RNG stream, so mining is unchanged.
  - `interval` (plan §3) and `worstcase` (plan §4, independent worst-case pair loss): on the six pairs of every mined
    tuple, bounds from the vote mode. `joint` (plan §4): exact integer allocation of MHIST's 7 readers (MILP; Step 1
    found the LP relaxation identical on every MHIST tuple), maximiser held fixed per step (subgradient); tuples with
    ≤ 2 split-vote images use the closed form (identical by construction, tested on 500 cases).
  - Vote modes: MHIST counts only. Gleason (Batch 11, supported ordering only): `linked` (observed shared-reader
    agreement where ≥ 3 readers are shared, else counts bounds; as in the census and pilot), `permuted` (votes
    reassigned within each image, redrawn per seed: vote_seed = seed), `counts_only`. Votes of labelled training
    images only (LEAKAGE RULE).
  - Runs: MHIST draws 0–4 (seed = draw, as Batch 6), 6 losses → 30 runs. Gleason folds 0–2 × seeds 0–1 (budget:
    ~8 min per run), 3 vote modes → 18 runs. Baselines reused: `results/mhist/*_hsrl_soft`, `results/soft/*_hsrl_soft`.
  - Reading, fixed now. Primary metric balanced accuracy, paired with `hsrl_soft` on the same draw / fold and seed.
    1. A loss improves on HSRL's structural supervision if the mean gain is ≥ +1.0 point and the gain is positive in
       ≥ 4/5 MHIST draws.
    2. A `supported` gain is credited to the certificate only if `supported` also beats both matched controls by the
       same standard; otherwise it is "fewer or easier hinges".
    3. Joint compatibility matters only if `joint` beats `worstcase` by the same standard.
    4. Gleason: reader linkage matters if `supported_linked` − `supported_permuted` is ≥ +1.0 point on average,
       positive in ≥ 5/6 runs and in all 3 fold means. Counts-only is reported alongside.
    Secondary: accuracy, AUROC, Brier, split-vote accuracy, pseudo-label precision at equal coverage. With 5 draws /
    6 runs only effects of about 1–2 points or more are detectable; a null means "no effect that large".
- **D46 Five more MHIST draws and an HSRL rerun control (user go-ahead 2026-11-01, "yes do both"; recorded before
  running).** Batch 13 (`results/mhist_d10/`) and Batch 14 (`results/mhist_rerun/`).
  - Why: on the D45 differences (paired SD about 1.5 points), the 95% interval is about ±1.9 points with 5 draws and
    ±1.1 with 10. A loss with no effect passes "≥ +1.0 and ≥ 4/5" by chance about 6% of the time, and "≥ +1.0 and
    ≥ 8/10" about 1%.
  - Data: draws 5–9 from `data/mhist_prepare.py --draws 10` (draw k uses seed [20261031, k]). Draws 0–4 were
    regenerated and checked byte-identical before draws 5–9 were added. Two draws' labelled sets share 6–14% of their
    images (mean 9.9%). All draws use the same official test set (977 images), so more draws average over labelled
    sets and training randomness, not over test images.
  - Runs, draws 5–9 (seed = draw, settings as Batches 6, 7 and 10): `hsrl`, `hsrl_soft` (reuses that draw's `hsrl`
    Stage I), `supervised`, `supervised_soft` and the six D45 losses.
  - Rerun control, draws 0–9: HSRL retrained with seed 100 + k (`hsrl_rerun`, then `hsrl_soft_rerun` reusing its
    Stage I). It measures how far a plain rerun of HSRL moves the score. §12.12's "gains only on HSRL's weak draws"
    could be regression to the mean: after an unlucky HSRL run, any rerun tends to score higher.
  - Reading, fixed now (balanced accuracy, paired with `hsrl_soft` on the same draw):
    1. Primary: D45 criteria 1–3 on 10 draws, with "mean ≥ +1.0 and positive in ≥ 8/10 draws".
    2. Replication: draws 5–9 alone, with the original rule (≥ +1.0 and ≥ 4/5). The 5-draw verdicts in §12.12 stand
       as recorded; all three views are reported.
    3. Weak-draw pattern: weak draws = the 5 draws with the lowest `hsrl_soft` balanced accuracy. The pattern counts
       as real only if, on the weak draws, the mean of the six losses beats `hsrl_soft_rerun` by ≥ +1.0 point.
       Otherwise it is attributed to rerun noise.
    4. Secondary: HSRL − supervised (hard and soft targets) on 10 draws.
- **D47 Certified gap as a margin (plan §3: "its conversion into a ranking loss is a modelling choice that needs
  sensitivity analysis"; user go-ahead 2026-11-01; recorded before running).** Batch 12 (`results/mhist_margin/`,
  `results/gleason_margin/`). Only the margin of supported ordering changes (`stage1.margin`). Hinge selection,
  mining, schedule and Stages II–III are as in `supported` (D45). Nothing is tuned.
  - `gap`: margin = HSRL's margin (α, β, γ) × the guaranteed agreement gap g = L_x − U_y ∈ (0, 1]. It is never larger
    than HSRL's; weakly supported orderings get a small margin.
  - `gap_shuffled` (control): the same margins, permuted at random among the term's certified tuples in each batch.
    Same hinges and same margin distribution; only the tuple-specific information is removed.
  - `similarity`: the gap on the plan's similarity scale t = 1 − d/4, i.e. a squared-distance margin of 4g (up to 4,
    larger than HSRL's).
  - Runs: MHIST draws 0–9 × {gap, gap_shuffled, similarity}; Gleason linked votes, folds 0–2 × seeds 0–1, `gap` only.
  - Reading, fixed now (balanced accuracy, paired):
    1. MHIST: a margin variant improves on HSRL if it beats `hsrl_soft` by ≥ +1.0 on average and in ≥ 8/10 draws.
    2. The margin itself is credited only if `gap` also beats `supported` (fixed margins) and `gap_shuffled` by the
       same standard.
    3. Gleason: `gap` − `supported_linked` ≥ +1.0, positive in ≥ 5/6 runs and in all three fold means.
    Secondary as in D45.
