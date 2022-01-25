import glob
import onnx
import pandas as pd
import torch

from make_me_rich.pipelines.training_model import PricePredictor
from make_me_rich.pipelines.training_model import LSTMDataLoader

from typing import Any, Dict, List, Tuple


def convert_model(
    train_sequences: List[Tuple[pd.DataFrame, float]],
    val_sequences: List[Tuple[pd.DataFrame, float]],
    test_sequences: List[Tuple[pd.DataFrame, float]],
    parameters: str
):
    """
    Convert trained model to ONNX.
    """
    model_path = [file for file in glob.glob(f"{parameters['dir_path']}/*.ckpt")][0]
    model = PricePredictor.load_from_checkpoint(model_path)
    data = LSTMDataLoader(
        train_sequences=train_sequences, 
        val_sequences=val_sequences, 
        test_sequences=test_sequences, 
        train_batch_size=parameters["train_batch_size"], 
        val_batch_size=parameters["val_batch_size"],
    )
    data.setup()
    input_batch = next(iter(data.train_dataloader()))
    input_sample = input_batch[0][0].unsqueeze(0)
    path_onnx_model = f"{parameters['dir_path']}/model.onnx"
    torch.onnx.export(
        model, input_sample, path_onnx_model,
        export_params=True,
        opset_version=11,
        input_names=["sequence"],
        output_names=["output"],
        dynamic_axes={
            "sequence": {0: "batch_size"},
            "output": {0: "batch_size"},
        },
    )
    onnx_model = onnx.load(path_onnx_model)
    onnx.checker.check_model(onnx_model)
