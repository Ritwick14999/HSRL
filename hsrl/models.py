"""f: EfficientNet-B2 backbone (timm, ImageNet weights); g: 2-layer MLP -> 128-d L2-normalised embedding;
h: linear classifier on backbone features (softmax applied in the loss / at prediction). g is unused at inference."""
import timm
import torch.nn as nn
import torch.nn.functional as F


class HSRLNet(nn.Module):
    def __init__(self, backbone="efficientnet_b2", pretrained=True, proj_hidden=None, proj_dim=128, n_classes=2):
        super().__init__()
        self.f = timm.create_model(backbone, pretrained=pretrained, num_classes=0, drop_rate=0.0, drop_path_rate=0.0)
        d = self.f.num_features
        hidden = proj_hidden or d
        self.g = nn.Sequential(nn.Linear(d, hidden), nn.ReLU(inplace=True), nn.Linear(hidden, proj_dim))
        self.h = nn.Linear(d, n_classes)

    def features(self, x):
        return self.f(x)

    def embed(self, feats):
        """Normalised embedding z (Eq. 1), computed in fp32."""
        return F.normalize(self.g(feats.float()), dim=1)

    def classify(self, feats):
        return self.h(feats.float())

    def forward(self, x):
        return self.classify(self.features(x))


def param_counts(model):
    n = lambda m: sum(p.numel() for p in m.parameters())
    return {"f": n(model.f), "g": n(model.g), "h": n(model.h), "f+h (inference)": n(model.f) + n(model.h),
            "total (training)": n(model)}
