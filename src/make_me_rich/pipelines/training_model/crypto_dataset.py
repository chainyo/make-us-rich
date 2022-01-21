import pandas as pd
import torch

from torch.utils.data import Dataset
from typing import List, Tuple


class CryptoDataset(Dataset):
    """
    Dataset class for the LSTM model used by PyTorch Lightning.
    """
    def __init__(self, sequences: List[Tuple[pd.DataFrame]]):
        self.sequences = sequences


    def __len__(self):
        return len(self.sequences)


    def __getitem__(self, index: int):
        sequence, label = self.sequences[index]
        return dict(
            sequence=torch.tensor(sequence.to_numpy()),
            label=torch.tensor(label).float(),
        )
