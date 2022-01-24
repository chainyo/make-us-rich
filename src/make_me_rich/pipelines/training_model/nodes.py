import pandas as pd

from pytorch_lightning import (
    Trainer, 
    callbacks,
    seed_everything,
)
from pytorch_lightning.loggers import WandbLogger
from typing import  Any, Dict, List, Tuple

from .model import PricePredictor
from .dataloader import LSTMDataLoader


logger = WandbLogger(project="make-me-rich")

def training_loop(
    train_sequences: List[Tuple[pd.DataFrame, float]], 
    val_sequences: List[Tuple[pd.DataFrame, float]],
    test_sequences: List[Tuple[pd.DataFrame, float]],
    parameters: Dict[str, Any],
):
    """
    Training loop for the LSTM model.

    Args:
        train_sequences: List of training sequences.
        val_sequences: List of validation sequences.
        test_sequences: List of test sequences.
        parameters: Dictionary of training parameters.
        dir_path: Path to store checkpoints.
    """
    seed_everything(42, workers=True)


    model = PricePredictor(
        batch_size=parameters["train_batch_size"],
        dropout_rate=parameters["dropout_rate"],
        hidden_size=parameters["hidden_size"],
        learning_rate=parameters["learning_rate"],
        number_of_features=parameters["number_of_features"],
        number_of_layers=parameters["number_of_layers"],
        run_on_gpu=parameters["run_on_gpu"],
    )

    data_module = LSTMDataLoader(
        train_sequences=train_sequences, 
        val_sequences=val_sequences,
        test_sequences=test_sequences,
        train_batch_size=parameters["train_batch_size"], 
        val_batch_size=parameters["val_batch_size"],
        train_workers=parameters["train_workers"],
        val_workers=parameters["val_workers"],
    )

    checkpoint_callback = callbacks.ModelCheckpoint(
        dirpath=parameters["dir_path"],
        filename="{epoch}-{val_loss:.2f}",
        save_top_k=1,
        verbose=True,
        monitor="val_loss",
        mode="min",
    )

    early_stopping_callback = callbacks.EarlyStopping(
        monitor="val_loss",
        patience=2
    )

    trainer = Trainer(
        max_epochs=parameters["max_epochs"],
        logger=logger,
        checkpoint_callback=checkpoint_callback,
        callbacks=[early_stopping_callback],
        gpus=0, # 0 by default, 1 for gpu user
        log_every_n_steps=parameters["log_n_steps"],
        progress_bar_refresh_rate=10,
        deterministic=True,
        accelerator="cpu",
    )

    trainer.fit(model, data_module)
    trainer.test(model, data_module)
