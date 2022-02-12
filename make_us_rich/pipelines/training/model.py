import torch
import torch.nn as nn
import pytorch_lightning as pl

from typing import Tuple, Dict


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
        run_on_gpu: bool,
    ):
        super().__init__()
        self.batch_size = batch_size
        self.dropout_rate = dropout_rate
        self.hidden_size = hidden_size
        self.n_features = number_of_features
        self.number_of_layers = number_of_layers
        self.run_on_gpu = run_on_gpu

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
        if self.run_on_gpu:
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
        run_on_gpu: bool,
        criterion: nn.Module = nn.MSELoss(),
    ) -> None:
        """
        Initialize the model.

        Parameters
        ----------
        batch_size: int
            Batch size for training.
        dropout_rate: float
            Dropout rate for the LSTM.
        hidden_size: int
            Hidden size for the LSTM.
        learning_rate: float
            Learning rate for the optimizer.
        number_of_features: int
            Number of features in the input.
        number_of_layers: int
            Number of layers in the LSTM.
        run_on_gpu: bool
            Whether to run the model on the GPU.
        criterion: nn.Module
            Loss function to use.

        Returns
        -------
        None
        """
        super().__init__()
        self.model = LSTMRegressor(
            batch_size, dropout_rate, hidden_size, number_of_features, number_of_layers, run_on_gpu,
        )
        self.learning_rate = learning_rate
        self.criterion = criterion
        self.save_hyperparameters()


    def forward(self, x, labels=None) -> Tuple[float, torch.Tensor]:
        """
        Forward pass through the model.

        Parameters
        ----------
        x: torch.Tensor
            Input data.
        labels: torch.Tensor
            Labels for the data.

        Returns
        -------
        loss: float
            Loss for the model.
        output: torch.Tensor
            Output of the model.
        """
        output = self.model(x)
        if labels is not None:
            loss = self.criterion(output, labels.unsqueeze(dim=1))
            return loss, output
        return output

        
    def training_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> Dict:
        """
        Training step.

        Parameters
        ----------
        batch: Tuple[torch.Tensor, torch.Tensor]
            Tuple of input data and labels.
        batch_idx: int
            Batch index.
        
        Returns
        -------
        Dict
            Dictionary with the train loss.
        """
        sequences, labels = batch
        loss, _ = self(sequences, labels)
        self.log("train/loss", loss, on_step=True, on_epoch=True)
        return {"loss": loss}


    def validation_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> Dict:
        """
        Validation step.

        Parameters
        ----------
        batch: Tuple[torch.Tensor, torch.Tensor]
            Tuple of input data and labels.
        batch_idx: int
            Batch index.
        
        Returns
        -------
        Dict
            Dictionary with the valid loss.
        """
        sequences, labels = batch
        loss, _ = self(sequences, labels)
        self.log("valid/loss", loss, on_step=True, on_epoch=True)
        return {"loss": loss}


    def test_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> Dict:
        """
        Test step.

        Parameters
        ----------
        batch: Tuple[torch.Tensor, torch.Tensor]
            Tuple of input data and labels.
        batch_idx: int
            Batch index.
        
        Returns
        -------
        Dict
            Dictionary with the test loss.
        """
        sequences, labels = batch
        loss, _ = self(sequences, labels)
        self.log("test/loss", loss, on_step=True, on_epoch=True)
        return {"loss": loss}


    def configure_optimizers(self) -> torch.optim.AdamW:
        """
        Configure the optimizer.

        Returns
        -------
        torch.optim.adamw.AdamW
            Optimizer.
        """
        return torch.optim.AdamW(self.parameters(), lr=self.learning_rate)
