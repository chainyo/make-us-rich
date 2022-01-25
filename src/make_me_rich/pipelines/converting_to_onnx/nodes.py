import glob
import onnx
import onnxruntime
import pandas as pd
import torch

from make_me_rich.pipelines.training_model import PricePredictor
from make_me_rich.pipelines.training_model import LSTMDataLoader

from typing import List, Tuple


def convert_model(
    train_sequences: List[Tuple[pd.DataFrame, float]],
    val_sequences: List[Tuple[pd.DataFrame, float]],
    test_sequences: List[Tuple[pd.DataFrame, float]],
    parameters: str,
    dir_path: str,
    training_done: bool,
):
    """
    Convert trained model to ONNX.

    Args:
        train_sequences: List of training sequences.
        val_sequences: List of validation sequences.
        test_sequences: List of test sequences.
        parameters: Dictionary of training parameters.
        dir_path: Directory path where the model is saved.
        training_done: Flag to check if the training is done.
    """
    if training_done["training_done"] == True:
        model_path = [file for file in glob.glob(f"{dir_path}/*.ckpt")][0]
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
        path_onnx_model = f"{dir_path}/model.onnx"
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
    return {"conversion_done": True}


def validate_model(dir_path: str, conversion_done: bool):
    """
    Check if the converted model is valid.

    Args:
        dir_path: Directory path where the model is saved.
        conversion_done: Flag to check if the conversion is done.
    """
    if conversion_done["conversion_done"] == True:
        path_onnx_model = f"{dir_path}/model.onnx"
        onnx_model = onnx.load(path_onnx_model)
        try:
            onnx.checker.check_model(onnx_model)
        except onnx.checker.ValidationError as e:
            raise ValueError(f"ONNX model is not valid: {e}")
        else:
            return {"validation_done": True}


def test_model(dir_path: str, validation_done: bool):
    """
    Test the converted model.

    Args:
        dir_path: Directory path where the model is saved.
        validation_done: Flag to check if the validation is done.
    """
    if validation_done["validation_done"] == True:
        path_onnx_model = f"{dir_path}/model.onnx"
        onnx_model = onnx.load(path_onnx_model)
        try:
            onnx.checker.check_model(onnx_model)
        except onnx.checker.ValidationError as e:
            raise ValueError(f"ONNX model is not valid: {e}")
        else:
            return {"test_done": True}
