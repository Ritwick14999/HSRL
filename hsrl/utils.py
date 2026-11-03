import json
import random
from pathlib import Path

import numpy as np
import torch
import yaml


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def deep_update(base, upd):
    for k, v in upd.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            deep_update(base[k], v)
        else:
            base[k] = v
    return base


def load_config(path, overrides=()):
    """YAML config with optional `base:` file (deep-merged) and dotted key=value overrides."""
    cfg = yaml.safe_load(open(path))
    if "base" in cfg:
        base = load_config(cfg.pop("base"))
        cfg = deep_update(base, cfg)
    for o in overrides:
        k, v = o.split("=", 1)
        d = cfg
        keys = k.split(".")
        for kk in keys[:-1]:
            d = d.setdefault(kk, {})
        d[keys[-1]] = yaml.safe_load(v)
    return cfg


def save_yaml(obj, path):
    with open(path, "w") as f:
        yaml.safe_dump(obj, f, sort_keys=False)


def save_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=float)


def make_run_dir(cfg):
    d = cfg["data"]
    name = cfg.get("run_name") or f"{cfg['method']}_{d['dataset']}_fold{d.get('fold', 0)}_seed{cfg['seed']}"
    run_dir = Path(cfg.get("results_root", "results")) / name
    if run_dir.exists() and any(run_dir.iterdir()) and not cfg.get("overwrite", False):
        raise FileExistsError(f"{run_dir} exists; set run_name or overwrite=true")
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir
