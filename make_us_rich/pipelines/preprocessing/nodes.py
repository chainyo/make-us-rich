import pandas as pd

from pickle import dump
from typing import List, Tuple

from sklearn.preprocessing import MinMaxScaler


def extract_features_from_dataset(data: pd.DataFrame) -> pd.DataFrame:
    """
    Extract features from dataset.

    Parameters
    ----------
    data: pd.DataFrame
        Market chart data.
    
    Returns
    -------
    pd.DataFrame
        Pandas dataframe of features.
    """
    rows = []
    for _, row in data.iterrows():
        row_data = dict(
            day_of_week=row["timestamp"].dayofweek,
            day_of_month=row["timestamp"].day,
            week_of_year=row["timestamp"].week,
            month_of_year=row["timestamp"].month,
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            close_change=row["close"] - row["open"],
        )
        rows.append(row_data)
    return pd.DataFrame(rows)


def split_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Split data into training and test sets.

    Parameters
    ----------
    data: pd.DataFrame
        Market chart data.
    
    Returns
    -------
    pd.DataFrame
        Pandas dataframe of training and test data.
    """
    train_size = int(len(data) * 0.9)
    train_df, test_df = data[:train_size], data[train_size + 1:]
    return train_df, test_df


def scale_data(
    train_df: pd.DataFrame, test_df: pd.DataFrame, dir_path: str,
) -> pd.DataFrame:
    """
    Scale data to have a mean of 0 and a standard deviation of 1.

    Parameters
    ----------
    train_df: pd.DataFrame
        Training data.
    test_df: pd.DataFrame
        Test data.
    dir_path: str
        Directory path to save the scaler.
    
    Returns
    -------
    pd.DataFrame
        Scaled training and test data.
    """
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler.fit(train_df)

    scaled_train_df = pd.DataFrame(
        scaler.transform(train_df),
        index=train_df.index, 
        columns=train_df.columns,
    )
    scaled_test_df = pd.DataFrame(
        scaler.transform(test_df),
        index=test_df.index,
        columns=test_df.columns,
    )
    dump(scaler, open(f"{dir_path}/scaler.pkl", "wb"))
    return scaled_train_df, scaled_test_df


def create_sequences(
    input_data: pd.DataFrame, 
    target_column: str, 
    sequence_length: int,
    ) -> List[Tuple[pd.DataFrame, float]]:
    """
    Create sequences from the input data.

    Parameters
    ----------
    input_data: pd.DataFrame
        Pandas dataframe of input data.
    target_column: str
        Name of the column to predict.
    sequence_length: int
        Length of the sequence.
    
    Returns
    -------
    List[Tuple[pd.DataFrame, float]]
        List of sequences.
    """
    sequences = []
    size = len(input_data)
    for i in range(size - sequence_length):
        sequence = input_data[i: i + sequence_length]
        label_position = i + sequence_length
        label = input_data.iloc[label_position][target_column]
        sequences.append([sequence, label])
    return sequences


def split_train_and_val_sequences(
    sequences: List[Tuple[pd.DataFrame, float]],
    val_size: float,
) -> Tuple[List[Tuple[pd.DataFrame, float]]]:
    """
    Split sequences into training and validation sets.

    Parameters
    ----------
    sequences: List[Tuple[pd.DataFrame, float]]
        List of sequences.
    val_size: float
        Percentage of the data to use as validation.
    
    Returns
    -------
    Tuple[List[Tuple[pd.DataFrame, float]]]
        Tuple of training and validation sequences.
    """
    train_sequences, val_sequences = [], []
    for sequence, label in sequences:
        if len(train_sequences) < len(sequences) * (1 - val_size):
            train_sequences.append((sequence, label))
        else:
            val_sequences.append((sequence, label))
    return train_sequences, val_sequences
