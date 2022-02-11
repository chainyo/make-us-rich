import pandas as pd
import pytorch_lightning as pl

from torch.utils.data import DataLoader
from typing import List, Tuple

from make_us_rich.pipelines.training import CryptoDataset


class LSTMDataLoader(pl.LightningDataModule):
    """
    Data loader for the LSTM model.
    """
    def __init__(self,
        train_sequences: List[Tuple[pd.DataFrame, float]],
        val_sequences: List[Tuple[pd.DataFrame, float]],
        test_sequences: List[Tuple[pd.DataFrame, float]],
        train_batch_size: int,
        val_batch_size: int,
        train_workers: int = 2,
        val_workers: int = 1,
    ):
        """
        Initialize the data loader.

        Parameters
        ----------
        train_sequences: List[Tuple[pd.DataFrame, float]]
            List of training sequences.
        val_sequences: List[Tuple[pd.DataFrame, float]]
            List of validation sequences.
        test_sequences: List[Tuple[pd.DataFrame, float]]
            List of test sequences.
        train_batch_size: int
            Batch size for training.
        val_batch_size: int
            Batch size for validation.
        train_workers: int
            Number of workers for training.
        val_workers: int
            Number of workers for validation.
        """
        super().__init__()
        self.train_sequences = train_sequences
        self.val_sequences = val_sequences
        self.test_sequences = test_sequences
        self.train_batch_size = train_batch_size
        self.val_batch_size = val_batch_size
        self.train_workers = train_workers
        self.val_workers = val_workers
        self.test_workers = val_workers


    def setup(self, stage: str = None) -> None:
        """
        Load the data.

        Parameters
        ----------
        stage: str
            Name of the stage. 
        """
        self.train_dataset = CryptoDataset(self.train_sequences)
        self.val_dataset = CryptoDataset(self.val_sequences)
        self.test_dataset = CryptoDataset(self.test_sequences)

    
    def train_dataloader(self):
        """Return the training data loader."""
        return DataLoader(
            self.train_dataset, 
            batch_size=self.train_batch_size, 
            shuffle=False,
            num_workers=self.train_workers
        )


    def val_dataloader(self):
        """Return the validation data loader."""
        return DataLoader(
            self.val_dataset, 
            batch_size=self.val_batch_size, 
            shuffle=False,
            num_workers=self.val_workers
        )


    def test_dataloader(self):
        """Return the test data loader."""
        return DataLoader(
            self.test_dataset, 
            batch_size=self.val_batch_size, 
            shuffle=False,
            num_workers=self.test_workers
        )
