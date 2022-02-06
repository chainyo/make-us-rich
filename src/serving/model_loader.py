import os

from datetime import datetime
from dotenv import load_dotenv
from minio import Minio
from pathlib import Path


load_dotenv()


class ModelLoader:
    """
    Loader class for interacting with the Minio Object Storage API.
    """

    def __init__(self):
        self.client = Minio(
            os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=False
        )
        self.bucket = os.getenv("MINIO_BUCKET")
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)
        self.storage_path = Path("./models")
        self.update_date()
        self.update_model_files()


    def update_date(self):
        """
        Updates the date of the loader.
        """
        self.date = datetime.now().strftime("%Y-%m-%d")

    
    def _makedir(self, currency: str, compare: str):
        """
        Creates a directory for the model files if it doesn't exist.

        Parameters
        ----------
        currency: str
            Currency used in the model.
        compare: str
            Compare used in the model.
        """
        self.storage_path.joinpath(f"{currency}_{compare}").mkdir(exist_ok=True)


    def _download_files(self, currency: str, compare: str):
        """
        Downloads model and features engineering files from Minio.

        Parameters
        ----------
        currency: str
            Currency used in the model.
        compare: str
            Compare used in the model.
        """
        self._makedir(currency, compare)
        self.client.fget_object(
            self.bucket,
            f"{self.date}/{currency}_{compare}/model.onnx",
            f"{self.storage_path}/{currency}_{compare}/model.onnx"
        )
        self.client.fget_object(
            self.bucket,
            f"{self.date}/{currency}_{compare}/scaler.pkl",
            f"{self.storage_path}/{currency}_{compare}/scaler.pkl"
        )


    def _get_list_of_available_models(self):
        """
        Looks for available models in the Minio bucket based on the date.

        Returns
        -------
        list
            List of avaialble models in the Minio bucket.
        """
        available_models = self.client.list_objects(self.bucket, prefix=self.date, recursive=True)
        return list(set([model.object_name.split("/")[1] for model in available_models]))


    def update_model_files(self):
        """
        Updates the model files in the serving models directory.
        """
        for model in self._get_list_of_available_models():
            self._download_files(model.split("_")[0], model.split("_")[1])
