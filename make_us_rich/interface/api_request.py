import requests

from typing import Dict

from make_us_rich.utils import load_env


class ApiRequest:
    """
    Class that handles the API requests for the interface
    """
    def __init__(self):
        self._config = load_env("api")
        self.url = self._config["URL"]

    
    def prediction(self, currency:str, compare:str, token: str) -> Dict:
        """
        Predict endpoint.

        Parameters
        ----------
        currency: str
            Currency used in the model.
        compare: str
            Compare used in the model.
        token: str
            API token of the user.
        
        Returns
        -------
        Dict
            Dictionary containing the data and the prediction.
        """
        return requests.put(
            f"{self.url}/predict", 
            params={"currency": currency, "compare": compare, "token": token}
        ).json()


    def number_of_available_models(self) -> Dict:
        """
        Number of available models endpoint.

        Returns
        -------
        Dict
            Dictionary containing the number of available models.
        """
        return requests.get(f"{self.url}/check_models_number").json()
