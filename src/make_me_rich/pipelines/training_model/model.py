import torch
import torch.nn as nn
import pytorch_lightning as pl


class LSTMRegressor(nn.Module):
    """
    Standard LSTM model with PyTorch Lightning.
    """
    def __init__(self,
        batch_size: int,
        dropout_rate: float,
        hidden_size: int,
        number_of_features: int,
        number_of_layers: int,
    ):
        super().__init__()
        self.batch_size = batch_size
        self.dropout_rate = dropout_rate
        self.hidden_size = hidden_size
        self.n_features = number_of_features
        self.number_of_layers = number_of_layers

        self.lstm = nn.LSTM(
            batch_first=True,
            dropout=self.dropout_rate,
            hidden_size=self.hidden_size,
            input_size=self.n_features,
            num_layers=self.number_of_layers,
        )

        self.regressor = nn.Linear(self.hidden_size, 1)


    def forward(self, x):
        """
        Forward pass through the model.

        lstm_out = (batch_size, sequence_length, hidden_size)
        """
        self.lstm.flatten_parameters()
        _, (hidden, _) = self.lstm(x)
        out = hidden[-1]
        return self.regressor(out)


class PricePredictor(pl.LightningModule):
    """
    Training model with PyTorch Lightning.
    """
    def __init__(self,
        batch_size: int,
        dropout_rate: float,
        hidden_size: int,
        learning_rate: float,
        number_of_features: int,
        number_of_layers: int,
        criterion: nn.Module = nn.MSELoss(),
    ):
        super().__init__()
        self.model = LSTMRegressor(
            batch_size, dropout_rate, hidden_size, number_of_features, number_of_layers,
        )
        self.learning_rate = learning_rate
        self.criterion = criterion


    def forward(self, x, labels=None):
        output = self.model(x)
        if labels is None:
            loss = self.criterion(output, labels.unsqueeze(dim=1))
        else: loss = 0
        return loss, output

        
    def training_step(self, batch, batch_idx):
        sequences, labels = batch
        loss, outputs = self(sequences, labels)
        self.log("train_loss", loss, on_step=True, on_epoch=True)
        return {"loss": loss}


    def validation_step(self, batch, batch_idx):
        sequences, labels = batch
        loss, outputs = self(sequences, labels)
        self.log("val_loss", loss, on_step=True, on_epoch=True)
        return {"loss": loss}


    def test_step(self, batch, batch_idx):
        sequences, labels = batch
        loss, outputs = self(sequences, labels)
        self.log("test_loss", loss, on_step=True, on_epoch=True)
        return {"loss": loss}


    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=self.learning_rate)
