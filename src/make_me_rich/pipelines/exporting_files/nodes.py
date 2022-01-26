from minio import Minio
from typing import Dict, Tuple


def upload_files(
    currency: str,
    compare: str,
    access_key: str,
    secret_key: str,
    endpoint: str,
    bucket: str,
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
    access_key: str
        Access key for the Minio server.
    secret_key: str
        Secret key for the Minio server.
    endpoint: str
        Endpoint for the Minio server.
    bucket: str
        Bucket to upload files to.
    validation: Dict[Tuple[str, bool], Tuple[str, str]]
        Dictionary of outputs from the validation step.
    dir_path: str
        Directory path where the model files are saved.
    """
    if validation["validation_done"] == True:
        client = Minio(
            endpoint, 
            access_key=access_key, 
            secret_key=secret_key, 
            secure=False
        )
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
        model_path = f"{dir_path}/model.onnx"
        client.fput_object(
            bucket_name=bucket,
            object_name=f"{currency}_{compare}/model.onnx",
            file_path=model_path,
        )
        scaler_path = f"{dir_path}/scaler.pkl"
        client.fput_object(
            bucket_name=bucket,
            object_name=f"{currency}_{compare}/scaler.pkl",
            file_path=scaler_path,
        )
    return {"upload_done": True}
    