import pandas as pd

from pytorch_lightning import Trainer, seed_everything
from typing import Dict

from .model import LSTMRegressor
from .dataloader import LSTMDataLoader


def training_loop(data: pd.DataFrame, parameters: Dict):
    """
    Training loop for the LSTM model.

    Args:
        parameters: The parameters for the LSTM model.
    """
    seed_everything(1)

    trainer = Trainer(
        max_epochs=parameters["max_epochs"],
        logger=False,
        gpus=0,
        row_log_interval=1,
        progress_bar_refresh_rate=2,
    )

    model = LSTMRegressor(
        batch_size=parameters["batch_size"],
        criterion=parameters["criterion"],
        dropout_rate=parameters["dropout_rate"],
        hidden_size=parameters["hidden_size"],
        learning_rate=parameters["learning_rate"],
        n_features=parameters["n_features"],
        number_of_layers=parameters["number_of_layers"],
        sequence_length=parameters["sequence_length"],
    )

    data_module = LSTMDataLoader(
        data=data, batch_size=parameters["batch_size"], sequence_length=parameters["sequence_length"],
    )

    trainer.fit(model, data_module)
    trainer.test(model, data_module)
