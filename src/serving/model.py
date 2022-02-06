import numpy as np
import onnxruntime

from pathlib import PosixPath
from pickle import load
from sklearn.preprocessing import MinMaxScaler

class OnnxModel:

    def __init__(self, model_path: str, scaler_path: str):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model_name = str(self.model_path.parent).split("/")[-1]
        self.model = onnxruntime.InferenceSession(str(model_path))
        self.scaler = self._load_scaler()
        self.descaler = self._create_descaler()

    
    def __repr__(self) -> str:
        return f"<OnnxModel: {self.model_name}>"

    
    def predict(self, sample):
        """
        Predicts the sample.
        """
        raise NotImplementedError


    def _load_scaler(self) -> MinMaxScaler:
        """
        Loads the scaler from the model files.
        """
        return load(open(self.scaler_path, "rb"))

    
    def _create_descaler(self) -> MinMaxScaler:
        """
        Creates a descaler.
        """
        descaler = MinMaxScaler()
        descaler.min_, descaler.scale_ = self.scaler.min_[-1], self.scaler.scale_[-1]
        return descaler

    
    def _descaling_sample(self, sample) -> None:
        """
        Descalings the sample.
        """
        values_2d = np.array(sample)[:, np.newaxis]
        return self.descaler.inverse_transform(values_2d).flatten()
        

