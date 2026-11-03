"""Phase 4: tuple census for HSRL's implied orderings, with linked-reader and counts-only verdicts.

For each HSRL term the implied ordering is   term1: s_ap > s_an   term2: s_ap > s_nc   term3: s_ap > s_ac
where s_ij is the agreement between images i and j.

Linked verdict (needs reader identities): s_ij = fraction of shared readers (valid votes on both) who give both
  images the same class. Pairs with < min_shared shared readers are skipped. Ordering s_x > s_y is
  supported / violated / tie.
Counts-only verdict (q only): L_ij = |q_i + q_j - 1|, U_ij = 1 - |q_i - q_j|. s_x > s_y is certified if L_x > U_y,
  contradicted if L_y > U_x, undecided otherwise. CAVEAT: these bounds assume a common reader panel; in Gleason
  the panel varies per core (and per patch through 'none' labels), so they are bounds under a common-panel model only.

Tuple sets: (A) n_random random tuples drawn from the labelled set with HSRL's role constraints (a, p same majority
class, p != a; n, c the other class, n != c); (B) tuples actually mined in Stage I (from tuples_stage1.csv),
for the chosen epoch(s).

All votes used here belong to labelled training patches (analysis only). Hidden labels of the unlabelled pool are
used only in the final pseudo-label analysis, which is evaluation.

Usage: python -I analysis/tuple_census.py --run results/hsrl_gleason_fold0_seed0
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import torch
import yaml
from sklearn.metrics import roc_auc_score

TERMS = {1: ("ap", "an"), 2: ("ap", "nc"), 3: ("ap", "ac")}
PAIRS = {"ap": ("a", "p"), "an": ("a", "n"), "nc": ("n", "c"), "ac": ("a", "c")}
EPS = 1e-9


def load_labelled(cfg):
    from hsrl.data.gleason import labels_set_name
    d = cfg["data"]
    if d.get("dataset") == "mhist":   # counts only: r1..r6 are empty, so every linked verdict is "skipped"
        fold_dir = Path(d["processed_root"]) / f"labels_p{d.get('labelled_pct', 10)}" / "folds" / f"fold{d['fold']}"
    else:
        fold_dir = Path(d["processed_root"]) / f"p{d['tile_size']}" / labels_set_name(d) / "folds" / f"fold{d['fold']}"
    cols = [f"r{k}" for k in range(1, 7)]
    lab = pd.read_csv(fold_dir / "labelled_list.csv", dtype={c: "Int64" for c in cols})
    lab = lab[lab.train_majority == 1].reset_index(drop=True)
    V = lab[cols].fillna(-1).to_numpy(dtype=np.int64)
    return lab, V, lab.q.to_numpy(float), lab.majority_label.astype(int).to_numpy()


def random_tuples(y, n, rng):
    idx = {k: np.flatnonzero(y == k) for k in np.unique(y)}
    a = rng.integers(0, len(y), n)
    out = {"a": a, "p": np.empty(n, int), "n": np.empty(n, int), "c": np.empty(n, int)}
    for k in idx:
        sel = np.flatnonzero(y[a] == k)
        same, other = idx[k], np.concatenate([idx[j] for j in idx if j != k])
        p = same[rng.integers(0, len(same), len(sel))]
        clash = p == a[sel]
        while clash.any():
            p[clash] = same[rng.integers(0, len(same), clash.sum())]
            clash = p == a[sel]
        nn = other[rng.integers(0, len(other), len(sel))]
        cc = other[rng.integers(0, len(other), len(sel))]
        clash = cc == nn
        while clash.any():
            cc[clash] = other[rng.integers(0, len(other), clash.sum())]
            clash = cc == nn
        out["p"][sel], out["n"][sel], out["c"][sel] = p, nn, cc
    return out


def pair_stats(V, q, i, j):
    vi, vj = V[i], V[j]
    shared = (vi >= 0) & (vj >= 0)
    n_sh = shared.sum(1)
    same = (shared & (vi == vj)).sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        s = np.where(n_sh > 0, same / np.maximum(n_sh, 1), np.nan)
    L = np.abs(q[i] + q[j] - 1)
    U = 1 - np.abs(q[i] - q[j])
    return {"s": s, "n_shared": n_sh, "L": L, "U": U}


def verdicts(V, q, tup, min_shared):
    ps = {name: pair_stats(V, q, tup[u], tup[v]) for name, (u, v) in PAIRS.items()}
    out = {}
    for t, (x, y) in TERMS.items():
        X, Y = ps[x], ps[y]
        ok = (X["n_shared"] >= min_shared) & (Y["n_shared"] >= min_shared)
        lv = np.full(len(X["s"]), "skipped", dtype=object)
        diff = X["s"] - Y["s"]
        lv[ok & (diff > EPS)] = "supported"
        lv[ok & (diff < -EPS)] = "violated"
        lv[ok & (np.abs(diff) <= EPS)] = "tie"
        cv = np.full(len(X["s"]), "undecided", dtype=object)
        cv[X["L"] > Y["U"] + EPS] = "certified"
        cv[Y["L"] > X["U"] + EPS] = "contradicted"
        out[t] = {"linked": lv, "counts": cv, "s_x": X["s"], "s_y": Y["s"]}
    return out, ps


def summarise(name, ver, ps, min_shared):
    rows, cross = [], {}
    for t, v in ver.items():
        lv, cv = pd.Series(v["linked"]), pd.Series(v["counts"])
        ev = lv != "skipped"
        n = len(lv)
        r = {"set": name, "term": t, "ordering": f"s_{TERMS[t][0]} > s_{TERMS[t][1]}", "n_tuples": n,
             "pct_certified": 100 * (cv == "certified").mean(), "pct_contradicted": 100 * (cv == "contradicted").mean(),
             "pct_undecided": 100 * (cv == "undecided").mean(),
             "n_linked_evaluable": int(ev.sum()), "n_linked_skipped": int((~ev).sum()),
             "pct_supported": 100 * (lv[ev] == "supported").mean(), "pct_violated": 100 * (lv[ev] == "violated").mean(),
             "pct_tie": 100 * (lv[ev] == "tie").mean()}
        for c in ("undecided", "certified", "contradicted"):
            m = ev & (cv == c)
            r[f"pct_linked_violated_given_{c}"] = 100 * (lv[m] == "violated").mean() if m.any() else float("nan")
            r[f"n_{c}_evaluable"] = int(m.sum())
        rows.append(r)
        cross[t] = pd.crosstab(cv, lv).to_dict()
    pair_info = {k: {"mean_shared": float(v["n_shared"].mean()),
                     f"n_pairs_lt{min_shared}_shared": int((v["n_shared"] < min_shared).sum()),
                     "n_pairs": int(len(v["n_shared"]))} for k, v in ps.items()}
    return rows, cross, pair_info


@torch.no_grad()
def embed_patches(run_dir, cfg, df, device):
    from hsrl.data import ImageDataset, build_transforms
    from hsrl.models import HSRLNet
    model = HSRLNet(n_classes=2, **{**cfg["model"], "pretrained": False}).to(device)
    model.load_state_dict(torch.load(run_dir / "model_stage1.pt", map_location=device))
    model.eval()
    image_root = cfg["data"].get("image_root") or cfg["data"]["processed_root"]   # MHIST images live in data/mhist
    ds = ImageDataset(df, image_root, build_transforms(cfg["augment"], train=False))
    dl = torch.utils.data.DataLoader(ds, batch_size=128, num_workers=0)
    zs = []
    for b in dl:
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
            f = model.features(b["image"].to(device))
        zs.append(model.embed(f).cpu())
    return torch.cat(zs)


def perm_test_auc(score, wrong, rng, n_perm=2000):
    if wrong.sum() == 0 or wrong.all():
        return float("nan"), float("nan")
    auc = roc_auc_score(wrong, score)
    null = np.array([roc_auc_score(rng.permutation(wrong), score) for _ in range(n_perm)])
    return float(auc), float((np.abs(null - 0.5) >= abs(auc - 0.5)).mean())


def rank_corr(x, y):
    x, y = pd.Series(x).rank(), pd.Series(y).rank()
    return float(np.corrcoef(x, y)[0, 1])


def _resid(r, c):
    A = np.column_stack([np.ones_like(c), c])
    return r - A @ np.linalg.lstsq(A, r, rcond=None)[0]


def core_perm_corr(err, rate, rng, control=None, n_perm=5000):
    """Spearman (or partial Spearman given `control`) between core error rate and core rate; two-sided
    permutation p-value over cores."""
    if len(err) < 4:
        return float("nan"), float("nan")
    re, rr = pd.Series(err).rank().to_numpy(float), pd.Series(rate).rank().to_numpy(float)
    if control is not None:
        rc = pd.Series(control).rank().to_numpy(float)
        re, rr = _resid(re, rc), _resid(rr, rc)
    corr = lambda a, b: float(np.corrcoef(a, b)[0, 1]) if a.std() > 0 and b.std() > 0 else float("nan")
    r = corr(re, rr)
    null = np.array([corr(re, rng.permutation(rr)) for _ in range(n_perm)])
    return r, float((np.abs(null) >= abs(r)).mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--n-random", type=int, default=100_000)
    ap.add_argument("--min-shared", type=int, default=3)
    ap.add_argument("--epochs", default="last", help="'last', 'first', 'all' or comma list for tuple set B")
    ap.add_argument("--knn", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--min-core-patches", type=int, default=5)
    args = ap.parse_args()
    run_dir = Path(args.run)
    cfg = yaml.safe_load(open(run_dir / "config.yaml"))
    out = run_dir / "census"
    out.mkdir(exist_ok=True)
    rng = np.random.default_rng(args.seed)

    lab, V, q, y = load_labelled(cfg)
    pos = {pid: i for i, pid in enumerate(lab.patch_id)}
    log = pd.read_csv(run_dir / "tuples_stage1.csv")
    for c in ("anchor_id", "pos_id", "neg_id", "conf_id"):
        assert log[c].isin(pos).all(), f"{c}: tuple id outside the labelled set"
    epochs = sorted(log.epoch.unique())
    sel = {"last": [epochs[-1]], "first": [epochs[0]], "all": epochs}.get(args.epochs) or [int(e) for e in args.epochs.split(",")]

    sets = {"A_random": random_tuples(y, args.n_random, rng)}
    for e in sel:
        L = log[log.epoch == e]
        sets[f"B_mined_epoch{e}"] = {"a": L.anchor_id.map(pos).to_numpy(), "p": L.pos_id.map(pos).to_numpy(),
                                     "n": L.neg_id.map(pos).to_numpy(), "c": L.conf_id.map(pos).to_numpy(),
                                     "active": {t: L[f"t{t}_active"].to_numpy().astype(bool) for t in TERMS}}
    all_rows, crosses, pairinfo, active_rows = [], {}, {}, []
    for name, tup in sets.items():
        ver, ps = verdicts(V, q, tup, args.min_shared)
        rows, cross, pinfo = summarise(name, ver, ps, args.min_shared)
        all_rows += rows
        crosses[name], pairinfo[name] = cross, pinfo
        if "active" in tup:   # mined tuples: does the hinge actually fire on violated orderings?
            for t in TERMS:
                lv = pd.Series(ver[t]["linked"])
                for state, m in (("active", tup["active"][t]), ("inactive", ~tup["active"][t])):
                    ev = m & (lv != "skipped").to_numpy()
                    active_rows.append({"set": name, "term": t, "hinge": state, "n": int(m.sum()),
                                        "n_evaluable": int(ev.sum()),
                                        "pct_violated": 100 * float((lv[ev] == "violated").mean()) if ev.any() else float("nan"),
                                        "pct_supported": 100 * float((lv[ev] == "supported").mean()) if ev.any() else float("nan")})
    table = pd.DataFrame(all_rows)
    table.to_csv(out / "census_table.csv", index=False)
    pd.DataFrame(active_rows).to_csv(out / "census_active_vs_verdict.csv", index=False)

    # ---- per-patch involvement in violated / undecided tuples (all logged epochs) -----------------------------
    full = {"a": log.anchor_id.map(pos).to_numpy(), "p": log.pos_id.map(pos).to_numpy(),
            "n": log.neg_id.map(pos).to_numpy(), "c": log.conf_id.map(pos).to_numpy()}
    ver, _ = verdicts(V, q, full, args.min_shared)
    nviol, nund, ninv = np.zeros(len(lab)), np.zeros(len(lab)), np.zeros(len(lab))
    for t, v in ver.items():
        viol = v["linked"] == "violated"
        und = v["counts"] == "undecided"
        for r in "apnc":
            np.add.at(ninv, full[r], 1)
            np.add.at(nviol, full[r], viol)
            np.add.at(nund, full[r], und)
    patch = pd.DataFrame({"patch_id": lab.patch_id, "core_id": lab.core_id, "q": q, "label": y,
                          "n_involvements": ninv, "viol_rate": np.where(ninv > 0, nviol / np.maximum(ninv, 1), np.nan),
                          "undecided_rate": np.where(ninv > 0, nund / np.maximum(ninv, 1), np.nan)})
    patch.to_csv(out / "labelled_patch_involvement.csv", index=False)

    # ---- are wrong-but-confident pseudo-labels concentrated near such patches? (evaluation only) -------------
    conc = {}
    pl_path = run_dir / "pseudo_labels_round0.csv"
    if pl_path.exists() and (run_dir / "model_stage1.pt").exists():
        from hsrl.data import load_dataset
        data = load_dataset(cfg["data"])
        hidden = data.eval_labels("unlabelled")[["patch_id", "core_id", "majority_label", "tie", "unanimous"]]
        pl = pd.read_csv(pl_path).merge(hidden, on="patch_id")
        acc = pl[(pl.accepted == 1) & ~pl.tie.astype(bool)].reset_index(drop=True)
        acc["wrong"] = (acc.pseudo != acc.majority_label.astype(int)).astype(int)
        conc["n_accepted_nontie"] = int(len(acc))
        conc["n_wrong_confident"] = int(acc.wrong.sum())
        if len(acc) and 0 < acc.wrong.sum() < len(acc):
            dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            unl = data.unlabelled.set_index("patch_id").loc[acc.patch_id].reset_index()
            zl = embed_patches(run_dir, cfg, lab, dev)
            zu = embed_patches(run_dir, cfg, unl, dev)
            nn = torch.cdist(zu, zl).topk(args.knn, largest=False).indices.numpy()
            acc["nbr_viol_rate"] = patch.viol_rate.to_numpy()[nn].mean(1)
            acc["nbr_undecided_rate"] = patch.undecided_rate.to_numpy()[nn].mean(1)
            acc["nbr_label_disagree"] = (y[nn] != acc.pseudo.to_numpy()[:, None]).mean(1)
            acc.to_csv(out / "pseudo_label_neighbourhood.csv", index=False)
            has_linked = bool((V >= 0).any())   # MHIST: no reader identities, so no linked violation rate
            nbr_cols = ("nbr_viol_rate",) * has_linked + ("nbr_undecided_rate", "nbr_label_disagree")
            for col in nbr_cols:
                auc, p = perm_test_auc(acc[col].to_numpy(), acc.wrong.to_numpy(), rng)
                conc[col] = {"mean_wrong": float(acc.loc[acc.wrong == 1, col].mean()),
                             "mean_correct": float(acc.loc[acc.wrong == 0, col].mean()),
                             "auroc_predicting_wrong": auc, "perm_p": p}
                # control for the pseudo-labelled patch's own vote agreement (split votes drive both)
                for stratum, m in (("unanimous", acc.unanimous.astype(bool)), ("split_vote", ~acc.unanimous.astype(bool))):
                    s = acc[m]
                    a_s, p_s = perm_test_auc(s[col].to_numpy(), s.wrong.to_numpy(), rng)
                    conc[col][f"within_{stratum}"] = {"n": int(len(s)), "n_wrong": int(s.wrong.sum()),
                                                      "auroc_predicting_wrong": a_s, "perm_p": p_s}
            # PRIMARY (core level): labelled-patch violation rate of a core vs the pseudo-label error rate in that core.
            # Cores are the statistical unit (patches within a core are correlated). Permutation p-values permute
            # the core-level rates across cores; the partial correlation controls for the core's split-vote share.
            core_l = patch.groupby("core_id")[["viol_rate", "undecided_rate"]].mean()
            core_u = acc.assign(split=(~acc.unanimous.astype(bool)).astype(float)).groupby("core_id").agg(
                err=("wrong", "mean"), n=("wrong", "size"), split_frac=("split", "mean"))
            cj = core_u.join(core_l, how="inner")
            cj = cj[cj.n >= args.min_core_patches]
            if len(cj) >= 5:   # MHIST has no cores (core_id = image), so the core-level analysis does not apply
                cl = {"n_cores": int(len(cj)), "min_accepted_per_core": args.min_core_patches,
                      "n_patches": int(cj.n.sum())}
                for col in ("viol_rate", "undecided_rate"):
                    r, p = core_perm_corr(cj.err.to_numpy(), cj[col].to_numpy(), rng)
                    rp, pp = core_perm_corr(cj.err.to_numpy(), cj[col].to_numpy(), rng, control=cj.split_frac.to_numpy())
                    cl[col] = {"spearman": r, "perm_p": p, "partial_spearman_ctrl_split_frac": rp, "partial_perm_p": pp}
                conc["core_level"] = cl
                cj.to_csv(out / "core_level.csv")
            # own vote agreement of the pseudo-labelled patch (split vs unanimous)
            conc["error_rate_unanimous"] = float(acc.loc[acc.unanimous.astype(bool), "wrong"].mean())
            conc["error_rate_split_vote"] = float(acc.loc[~acc.unanimous.astype(bool), "wrong"].mean())

    summary = {"run": str(run_dir), "n_labelled": int(len(lab)), "min_shared": args.min_shared,
               "B_epochs": [int(e) for e in sel], "pair_info": pairinfo, "crosstabs": crosses, "pseudo_label_concentration": conc,
               "caveat": "counts-only bounds assume a common reader panel; Gleason readers vary per core and per patch"}
    with open(out / "census_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    pd.set_option("display.width", 250)
    print(table.round(2).to_string())
    print(pd.DataFrame(active_rows).round(2).to_string())
    print(json.dumps({"pair_info": pairinfo, "pseudo_label_concentration": conc}, indent=1, default=str))
    (out / "census_v2.done").write_text("ok")


if __name__ == "__main__":
    main()
