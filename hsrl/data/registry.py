"""Dataset adapters. Each adapter maps a `data:` config block to a SplitData."""
DATASETS = {}


def register(name):
    def deco(fn):
        DATASETS[name] = fn
        return fn
    return deco


def load_dataset(cfg):
    if cfg["dataset"] not in DATASETS:
        raise KeyError(f"unknown dataset {cfg['dataset']}; known: {sorted(DATASETS)}")
    return DATASETS[cfg["dataset"]](cfg)
