import numpy as np
import onnxruntime
import pandas as pd
import torch

from pickle import load
from sklearn.preprocessing import MinMaxScaler

from trainer.src.make_us_rich.pipelines.preprocessing_data.nodes import scale_data

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
        inputs = {self.model.get_inputs()[0].name: self._to_numpy(X)}
        results = self.model.run(None, inputs)[0][0]
        return results[0]


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


    def _load_scaler(self) -> MinMaxScaler:
        """
        Loads the scaler from the model files.
        """
        return load(open(self.scaler_path, "rb"))

    
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
        rows = []
        for _, row in sample.iterrows():
            row_data = dict(
                day_of_week=row["timestamp"].dayofweek,
                day_of_month=row["timestamp"].day,
                week_of_year=row["timestamp"].week,
                month_of_year=row["timestamp"].month,
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                close_change=float(row["close"]) - float(row["open"]),
            )
            rows.append(row_data)
        data = pd.DataFrame(rows)
        scaled_data = pd.DataFrame(
            self.model.scaler.transform(data), index=data.index, columns=data.columns
        )
        return torch.Tensor(scaled_data.values).unsqueeze(0)
    

    def _to_numpy(tensor: torch.Tensor):
        """
        Converts a tensor to numpy.

        Parameters
        ----------
        tensor: torch.Tensor
            Tensor to be converted.
        
        Returns
        -------
        numpy.ndarray
        """
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()
