import numpy as np
import onnxruntime
import pandas as pd
import torch

from pathlib import PosixPath
from pickle import load
from sklearn.preprocessing import MinMaxScaler

from make_us_rich.pipelines.preprocessing import extract_features_from_dataset
from make_us_rich.pipelines.converting import to_numpy


class OnnxModel:

    def __init__(self, model_path: PosixPath, scaler_path: PosixPath):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model_name = self.model_path.parent.parts[-1]
        self.model = onnxruntime.InferenceSession(str(model_path))
        self.scaler = self._load_scaler()
        self.descaler = self._create_descaler()

    
    def __repr__(self) -> str:
        return f"<OnnxModel: {self.model_name}>"

    
    def predict(self, sample: pd.DataFrame) -> float:
        """
        Predicts the close price based on the input sample.

        Parameters
        ----------
        sample: pd.DataFrame
            Input sample.

        Returns
        -------
        float
            Predicted close price.
        """
        X = self._preprocessing_sample(sample)
        inputs = {self.model.get_inputs()[0].name: to_numpy(X)}
        results = self.model.run(None, inputs)[0][0]
        return self._descaling_sample(results)


    def _create_descaler(self) -> MinMaxScaler:
        """
        Creates a descaler.

        Returns
        -------
        MinMaxScaler
        """
        descaler = MinMaxScaler()
        descaler.min_, descaler.scale_ = self.scaler.min_[-1], self.scaler.scale_[-1]
        return descaler

    
    def _descaling_sample(self, sample) -> None:
        """
        Descalings the sample.

        Parameters
        ----------
        sample: numpy.ndarray
            Sample to be descaled.
        
        Returns
        -------
        float
            Descaled sample.
        """
        values_2d = np.array(sample)[:, np.newaxis]
        return self.descaler.inverse_transform(values_2d).flatten()


    def _load_scaler(self) -> MinMaxScaler:
        """
        Loads the scaler from the model files.

        Returns
        -------
        MinMaxScaler
        """
        with open(self.scaler_path, "rb") as file:
            return load(file)

    
    def _preprocessing_sample(self, sample: pd.DataFrame) -> torch.tensor:
        """
        Preprocesses the input sample.

        Parameters
        ----------
        sample: pd.DataFrame
            Input sample.
        
        Returns
        -------
        torch.tensor
            Preprocessed sample.
        """
        data = extract_features_from_dataset(sample)
        scaled_data = pd.DataFrame(
            self.scaler.transform(data), index=data.index, columns=data.columns
        )
        return torch.Tensor(scaled_data.values).unsqueeze(0)
