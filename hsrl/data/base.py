"""Dataset-agnostic interface.

Every dataset (Gleason now, MHIST / PCam later) is exposed as a SplitData:
  labelled    patch_id, path, label (int), q (float), [r1..rK votes]   <- the ONLY vote-bearing table
  unlabelled  patch_id, path
  val, test   patch_id, path
  eval_labels(split)  ground-truth / vote table for evaluation and analysis only

LEAKAGE RULE: training code (hsrl/stages.py) reads labels and votes only from `labelled`.
`eval_labels` is used only by evaluation/analysis code, never inside a training loss or a sampling decision.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision.transforms import v2

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


@dataclass
class SplitData:
    name: str
    image_root: Path
    n_classes: int
    labelled: pd.DataFrame
    unlabelled: pd.DataFrame
    val: pd.DataFrame
    test: pd.DataFrame
    reader_cols: list = field(default_factory=list)
    _eval_labels: Callable = None

    def eval_labels(self, split):
        """Labels/votes for evaluation or post-hoc analysis. Never call from a training loss or sampler."""
        return self._eval_labels(split)

    def summary(self):
        lab = self.labelled
        return {"labelled": len(lab), "labelled_per_class": lab.label.value_counts().sort_index().to_dict(),
                "unlabelled": len(self.unlabelled), "val": len(self.val), "test": len(self.test)}


class Rot180:
    """Rotate by 180 degrees with probability p (the paper's '180° rotations')."""

    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, img):
        return v2.functional.rotate(img, 180) if torch.rand(1).item() < self.p else img


class Rot90:
    """Rotate by a random multiple of 90 degrees."""

    def __call__(self, img):
        k = int(torch.randint(0, 4, (1,)).item())
        return v2.functional.rotate(img, 90 * k) if k else img


def build_transforms(aug, train):
    t = [v2.ToImage()]
    if aug.get("resize"):   # optional input-size check (default: native tile size, no resize)
        t.append(v2.Resize(aug["resize"], antialias=True))
    if train:
        t += [v2.RandomHorizontalFlip(aug["hflip"]), v2.RandomVerticalFlip(aug["vflip"])]
        if aug["rotation"] == "rot180":
            t.append(Rot180(aug.get("rotation_p", 0.5)))
        elif aug["rotation"] == "rot90":
            t.append(Rot90())
        elif aug["rotation"] != "none":
            raise ValueError(aug["rotation"])
        cj = aug.get("color_jitter")
        if cj:
            t.append(v2.ColorJitter(**cj))
    t += [v2.ToDtype(torch.float32, scale=True), v2.Normalize(IMAGENET_MEAN, IMAGENET_STD)]
    return v2.Compose(t)


class ImageDataset(Dataset):
    """Returns {'idx', 'image'} plus 'target' (int) and 'soft' (float vector) when targets are given."""

    def __init__(self, df, image_root, transform, targets=None, soft=None):
        self.paths = [str(Path(image_root) / p) for p in df["path"]]
        self.transform = transform
        self.targets = None if targets is None else torch.as_tensor(list(targets), dtype=torch.long)
        self.soft = None if soft is None else torch.as_tensor(soft, dtype=torch.float32)

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, i):
        with Image.open(self.paths[i]) as im:
            img = self.transform(im.convert("RGB"))
        out = {"idx": i, "image": img}
        if self.targets is not None:
            out["target"] = self.targets[i]
        if self.soft is not None:
            out["soft"] = self.soft[i]
        return out
