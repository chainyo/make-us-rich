import torch
import torch.nn as nn
import pytorch_lightning as pl


class LSTMRegressor(pl.LightningModule):
    """
    Standard LSTM model with PyTorch Lightning.
    """
    def __init__(self,
        batch_size: int,
        criterion: nn.Module,
        dropout_rate: float,
        hidden_size: int,
        learning_rate: float,
        n_features: int,
        number_of_layers: int,
        sequence_length: int,
    ):
        super().__init__()
        self.batch_size = batch_size
        self.criterion = criterion
        self.dropout_rate = dropout_rate
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate
        self.n_features = n_features
        self.number_of_layers = number_of_layers
        self.sequence_length = sequence_length

        self.lstm = nn.LSTM(
            batch_first=True,
            dropout=self.dropout_rate,
            hidden_size=self.hidden_size,
            input_size=self.n_features,
            num_layers=self.number_of_layers,
        )

        self.linear = nn.Linear(self.hidden_size, 1)


    def forward(self, x):
        """
        Forward pass through the model.

        lstm_out = (batch_size, sequence_length, hidden_size)
        """
        lstm_out, _ = self.lstm(x)
        y_pred = self.linear(lstm_out[:,-1])
        return y_pred


    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)

    
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        result = pl.EvalResult(checkpoint_on=loss)
        result.log("val_loss", loss)
        return result


    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        result = pl.EvalResult(checkpoint_on=loss)
        result.log("val_loss", loss)
        return result


    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        result = pl.EvalResult()
        result.log("test_loss", loss)
        return result
