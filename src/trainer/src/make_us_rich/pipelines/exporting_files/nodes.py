from datetime import datetime
from minio import Minio
from typing import Dict, Tuple


def upload_files(
    currency: str,
    compare: str,
    validation: Dict[Tuple[str, bool], Tuple[str, str]],
    dir_path: str,
) -> None:
    """
    Uploads model and features engineering files to Minio.

    Parameters
    ----------
    currency: str
        Currency used in the model.
    compare: str
        Compare used in the model.
    validation: Dict[Tuple[str, bool], Tuple[str, str]]
        Dictionary of outputs from the validation step.
    dir_path: str
        Directory path where the model files are saved.
    """
    if validation["validation_done"] == True:
        client = Minio(
            "192.168.1.100:9101", 
            access_key="make-us-rich-pipeline", 
            secret_key="3Ggy3piB4936ZCmHzWWyGwPEGER3taFKYkUjyrCa", 
            secure=False
        )
        bucket = "make-us-rich"
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
        date = datetime.now().strftime("%Y-%m-%d")
        model_path = f"{dir_path}/model.onnx"
        client.fput_object(
            bucket_name=bucket,
            object_name=f"{date}/{currency}_{compare}/model.onnx",
            file_path=model_path,
        )
        scaler_path = f"{dir_path}/scaler.pkl"
        client.fput_object(
            bucket_name=bucket,
            object_name=f"{date}/{currency}_{compare}/scaler.pkl",
            file_path=scaler_path,
        )
    return {"upload_done": True}
    