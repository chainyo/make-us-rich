import pandas as pd

from datetime import datetime
from pathlib import Path
from typing import List

from make_us_rich.serving import OnnxModel
from make_us_rich.client import MinioClient


class ModelLoader:
    """
    Loader class for interacting with the Minio Object Storage API.
    """

    def __init__(self):
        self.client = MinioClient()
        self.session_models = {}
        self.storage_path = Path.cwd().joinpath("api", "models")
        self.update_date()
        self.update_model_files()


    def get_predictions(self, model_name: str, sample: pd.DataFrame) -> float:
        """
        Gets the predictions from the model.

        Parameters
        ----------
        model_name: str
            Name of the model.
        sample: pd.DataFrame
            Sample to predict.
        
        Returns
        -------
        float
            Predicted value.
        """
        if self._check_model_exists_in_session(model_name):
            model = self.session_models[model_name]["model"]
            return model.predict(sample)
        else:
            raise ValueError("Model not found in session.")


    def update_date(self):
        """
        Updates the date of the loader.
        """
        self.date = datetime.now().strftime("%Y-%m-%d")


    def update_model_files(self):
        """
        Updates the model files in the serving models directory.
        """
        for model in self._get_list_of_available_models():
            currency, compare = model.split("_")
            self._download_files(currency, compare)
            self._add_model_to_session_models(currency, compare)


    def _get_models_files_path(self, currency: str, compare: str):
        """
        Returns the path to the files in models directory.

        Parameters
        ----------
        currency: str
            Currency used in the model.
        compare: str
            Compare used in the model.
        
        Returns
        -------
        str
            Path to the model files.
        """
        model = self.storage_path.joinpath(f"{currency}_{compare}", "model.onnx")
        scaler = self.storage_path.joinpath(f"{currency}_{compare}", "scaler.pkl")
        return model, scaler

    
    def _makedir(self, currency: str, compare: str) -> None:
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


    def _download_files(self, currency: str, compare: str) -> None:
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
        self.client.download(
            self.client.bucket,
            f"{self.date}/{currency}_{compare}/model.onnx",
            f"{self.storage_path}/{currency}_{compare}/model.onnx"
        )
        self.client.download(
            self.client.bucket,
            f"{self.date}/{currency}_{compare}/scaler.pkl",
            f"{self.storage_path}/{currency}_{compare}/scaler.pkl"
        )


    def _get_list_of_available_models(self) -> List[str]:
        """
        Looks for available models in the Minio bucket based on the date.

        Returns
        -------
        List[str]
            List of available models.
        """
        available_models = self.client.list_objects(self.client.bucket, prefix=self.date, recursive=True)
        return list(set([model.object_name.split("/")[1] for model in available_models]))

    
    def _add_model_to_session_models(self, currency: str, compare: str) -> str:
        """
        Adds a new model to the model session.

        Parameters
        ----------
        currency: str
            Currency used in the model.
        compare: str
            Compare used in the model.
        
        Returns
        -------
        str
        """
        model_path, scaler_path = self._get_models_files_path(currency, compare)
        model = OnnxModel(model_path=model_path, scaler_path=scaler_path)
        self.session_models[f"{currency}_{compare}"] = {"model": model}
        return f"Model {model} added to session."


    def _check_model_exists_in_session(self, model_name: str) -> bool:
        """
        Checks if the model exists in the current session.

        Parameters
        ----------
        model_name: str
            Name of the model.
        
        Returns
        -------
        bool
        """
        if model_name in self.session_models.keys():
            return True
        return False
