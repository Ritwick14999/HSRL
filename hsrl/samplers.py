import numpy as np
from torch.utils.data import Sampler


class ClassBalancedBatchSampler(Sampler):
    """Batches with batch_size // K samples from each of the K classes. Each class is drawn without replacement
    from a reshuffled permutation, refilled when exhausted (so the minority class is cycled more often).
    One epoch = ceil(N / batch_size) batches. Labels come from the labelled set only."""

    def __init__(self, labels, batch_size, seed=0):
        self.labels = np.asarray(labels)
        self.classes = np.unique(self.labels)
        self.per_class = batch_size // len(self.classes)
        assert self.per_class >= 2, "need >= 2 samples per class per batch (positive + anchor)"
        self.n_batches = int(np.ceil(len(self.labels) / batch_size))
        self.rng = np.random.default_rng(seed)
        self.pools = {k: [] for k in self.classes}
        self.idx = {k: np.flatnonzero(self.labels == k) for k in self.classes}

    def _draw(self, k, m):
        out = []
        while len(out) < m:
            if not self.pools[k]:
                self.pools[k] = list(self.rng.permutation(self.idx[k]))
            out.append(self.pools[k].pop())
        return out

    def __iter__(self):
        for _ in range(self.n_batches):
            batch = []
            for k in self.classes:
                batch += self._draw(k, self.per_class)
            yield [int(i) for i in self.rng.permutation(batch)]

    def __len__(self):
        return self.n_batches
