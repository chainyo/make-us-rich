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
            "params:MINIO_ENDPOINT", 
            access_key="params:MINIO_ACCESS_KEY", 
            secret_key="params:MINIO_SECRET_KEY", 
            secure=False
        )
        bucket = "params:MINIO_BUCKET"
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
    