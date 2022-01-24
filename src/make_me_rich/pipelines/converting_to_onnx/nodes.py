import onnx
import torch

from make_me_rich.pipelines import PricePredictor
from make_me_rich.pipelines import LSTMDataLoader

from typing import Any, Dict


def convert_model(
    train_sequences: List[Tuple[pd.DataFrame, float]],
    val_sequences: List[Tuple[pd.DataFrame, float]],
    test_sequences: List[Tuple[pd.DataFrame, float]],
    parameters: str
):
    """
    Convert trained model to ONNX.
    """
    model = PricePredictor.load_from_checkpoint(parameters["dir_path"])
    data = LSTMDataLoader(
        train_sequences=train_sequences, 
        val_sequences=val_sequences, 
        test_sequences=test_sequences, 
        train_batch_size=parameters["train_batch_size"], 
        val_batch_size=parameters["val_batch_size"],
    )
    data.setup()
    input_batch = next(iter(data.train_dataloader()))
    path_onnx_model = f"{parameters['dir_path']}/model.onnx"
    torch.onnx.export(
        model, input_batch, path_onnx_model,
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
