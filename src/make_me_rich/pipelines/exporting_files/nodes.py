from minio import Minio
from typing import Dict


def upload_files(credentials: Dict[str, str], files: Dict[str, str]) -> None:
    """
    Uploads files to Minio.

    Args:
        access_key (str): Minio access key.
        secret_key (str): Minio secret key.
        endpoint (str): Minio endpoint.
    """
    client = Minio(
        credentials["ENDPOINT"], 
        access_key=credentials["ACCESS_KEY"], 
        secret_key=credentials["SECRET_KEY"], 
        secure=False
    )
    