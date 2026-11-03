"""Evaluation helpers. These read hidden labels via SplitData.eval_labels and must only run on predictions,
never inside training."""
import numpy as np
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, precision_score, roc_auc_score


def classification_metrics(prob1, y):
    pred = (prob1 > 0.5).astype(int)
    out = {"n": int(len(y)), "acc": accuracy_score(y, pred), "bal_acc": balanced_accuracy_score(y, pred),
           "macro_f1": f1_score(y, pred, average="macro"), "brier": float(np.mean((prob1 - y) ** 2)),
           "macro_precision": precision_score(y, pred, average="macro", zero_division=0)}   # macro recall = bal_acc
    out["auroc"] = roc_auc_score(y, prob1) if len(np.unique(y)) == 2 else float("nan")
    return {k: (round(float(v), 4) if k != "n" else v) for k, v in out.items()}


def evaluate_predictions(preds, labels):
    """Majority-label metrics on non-tie patches: overall, unanimous, split-vote."""
    m = preds.merge(labels, on="patch_id")
    m = m[~m.tie.astype(bool)]
    y = m.majority_label.astype(int).to_numpy()
    p = m.prob_1.to_numpy()
    out = {"overall": classification_metrics(p, y)}
    for name, sel in (("unanimous", m.unanimous.astype(bool)), ("split_vote", ~m.unanimous.astype(bool))):
        if sel.sum() > 0:
            out[name] = classification_metrics(p[sel.to_numpy()], y[sel.to_numpy()])
    return out


def pseudo_label_diagnostics(pseudo, labels, tau):
    """Coverage and precision of accepted pseudo-labels against hidden majority labels of the unlabelled pool."""
    m = pseudo.merge(labels, on="patch_id", how="left")
    acc = m[m.accepted == 1]
    out = {"tau": tau, "pool": int(len(m)), "accepted": int(len(acc)), "coverage": round(len(acc) / max(1, len(m)), 4)}
    def prec(df):
        df = df[~df.tie.astype(bool)]
        return {"n": int(len(df)), "precision": round(float((df.pseudo == df.majority_label.astype(int)).mean()), 4)
                if len(df) else None}
    out["overall"] = prec(acc)
    out["unanimous"] = prec(acc[acc.unanimous.astype(bool)])
    out["split_vote"] = prec(acc[~acc.unanimous.astype(bool)])
    out["tie_accepted"] = int(acc.tie.astype(bool).sum())
    return out
