import pandas as pd
import pytorch_lightning as pl
import torch

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader

from .timeseries_dataset import TimeseriesDataset


class LSTMDataLoader(pl.LightningDataModule):
    """
    Data loader for the LSTM model.
    """
    def __init__(self,
        data: pd.DataFrame,
        batch_size: int = 128,
        num_workers: int = 0,
        sequence_length: int = 1,
    ):
        super().__init__()
        self.data = data
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.sequence_length = sequence_length
        self.X_train = None
        self.y_train = None
        self.X_val = None
        self.y_val = None
        self.X_test = None
        self.y_test = None
        self.columns = None
        self.preprocessing = None


    def setup(self, stage:str = None):
        """
        Load the data.
        """
        if stage == "fit" and self.X_train is not None:
            return
        if stage == "test" and self.X_test is not None:
            return
        if stage is None and self.X_train is not None and self.X_test is not None:
            return

        
        X = self.data.dropna().copy()
        y = X["prices"].shift(-1).ffill()
        self.columns = X.columns

        X_cv, X_test, y_cv, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        X_train, X_val, y_train, y_val = train_test_split(X_cv, y_cv, test_size=0.25, shuffle=False)

        preprocessing = StandardScaler()
        preprocessing.fit(X_train)

        if stage == "fit" or stage is None:
            self.X_train = preprocessing.transform(X_train)
            self.y_train = y_train.values.reshape((-1, 1))
            self.X_val = preprocessing.transform(X_val)
            self.y_val = y_val.values.reshape((-1, 1))

        if stage == "test" or stage is None:
            self.X_test = preprocessing.transform(X_test)
            self.y_test = y_test.values.reshape((-1, 1))

    
    def train_dataloader(self):
        train_dataset = TimeseriesDataset(self.X_train, self.y_train, self.sequence_length)
        train_loader = DataLoader(
            train_dataset, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=False
        )
        return train_loader


    def val_dataloader(self):
        val_dataset = TimeseriesDataset(self.X_val, self.y_val, self.sequence_length)
        val_loader = DataLoader(
            val_dataset, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=False
        )
        return val_loader


    def test_dataloader(self):
        test_dataset = TimeseriesDataset(self.X_test, self.y_test, self.sequence_length)
        test_loader = DataLoader(
            test_dataset, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=False
        )
        return test_loader
