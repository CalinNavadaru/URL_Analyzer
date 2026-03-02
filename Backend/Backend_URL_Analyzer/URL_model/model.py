import lightning
import torch
import torch.nn as nn
from torchmetrics import MetricCollection
from torchmetrics.classification import BinaryAccuracy, BinaryPrecision, BinaryRecall, BinaryF1Score

from Backend_URL_Analyzer.URL_model.processing import PAD, char2idx


class AttentionPool(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.attn = nn.Linear(dim, 1)

    def forward(self, x, mask=None):
        scores = self.attn(x).squeeze(-1)

        if mask is not None:
            scores = scores.masked_fill(~mask, float("-inf"))

        weights = torch.softmax(scores, dim=1)
        pooled = torch.sum(x * weights.unsqueeze(-1), dim=1)
        return pooled

class Phishign_URL_CNN(lightning.LightningModule):
    def __init__(self, emb_dim=128, n_filters=128, dropout=0.3, lr=1e-3):
        super().__init__()
        self.save_hyperparameters()
        self.lr = lr
        vocab_size = len(char2idx) + 2
        self.emb = nn.Embedding(vocab_size, emb_dim, padding_idx=PAD)

        conv_layers = []
        in_ch = emb_dim
        k = 3
        for _ in range(3):
            conv_layers += [
                nn.Conv1d(in_ch, n_filters, k, padding=k//2),
                nn.LeakyReLU(),
                nn.BatchNorm1d(n_filters)
            ]
            in_ch = n_filters
            k += 2
        self.conv = nn.Sequential(*conv_layers)
        self.attn_pool = AttentionPool(n_filters)
        self.pool = nn.AdaptiveMaxPool1d(1)
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(2 * n_filters, 1)
        )

        self.crit = nn.BCEWithLogitsLoss()

        base_metrics = MetricCollection({
            "acc": BinaryAccuracy(),
            "prec": BinaryPrecision(),
            "rec": BinaryRecall(),
            "f1": BinaryF1Score()
        })

        self.train_metrics = base_metrics.clone(prefix="train_")
        self.val_metrics = base_metrics.clone(prefix="val_")
        self.test_metrics = base_metrics.clone(prefix="test_")

    def forward(self, x):
        mask = (x != PAD)

        x = self.emb(x).transpose(1, 2)
        x = self.conv(x)

        max_pooled = self.pool(x).squeeze(-1)

        attn_input = x.transpose(1, 2)
        attn_pooled = self.attn_pool(attn_input, mask)

        x = torch.cat([max_pooled, attn_pooled], dim=1)

        return self.head(x).squeeze(-1)

    def _shared_step(self, batch, stage):
        x, y = batch
        logits = self(x)
        loss = self.crit(logits, y.float())

        preds = torch.sigmoid(logits)
        metric_set = getattr(self, f"{stage}_metrics")

        metric_set.update(preds, y.long())
        self.log(f"{stage}_loss", loss, prog_bar=True, on_epoch=True, on_step=False)
        self.log_dict(metric_set, prog_bar=True, on_epoch=True, on_step=False)

        return loss

    def training_step(self, batch, batch_idx):
        return self._shared_step(batch, "train")

    def validation_step(self, batch, batch_idx):
        self._shared_step(batch, "val")

    def test_step(self, batch, batch_idx):
        self._shared_step(batch, "test")

    def on_train_epoch_end(self):
        self.train_metrics.reset()

    def on_validation_epoch_end(self):
        self.val_metrics.reset()

    def on_test_epoch_end(self):
        self.test_metrics.reset()

    def configure_optimizers(self):
        opt = torch.optim.AdamW(self.parameters(),
                                lr=self.lr,
                                weight_decay=1e-4)
        sch = torch.optim.lr_scheduler.ReduceLROnPlateau(opt,
                                                         mode="min",
                                                         patience=3)
        return {
            "optimizer": opt,
            "lr_scheduler": {
                "scheduler": sch,
                "monitor": "val_loss"
            }
        }
