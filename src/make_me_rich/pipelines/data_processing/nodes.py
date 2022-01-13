import requests
import pandas as pd

from datetime import datetime


def convert_timestamp(timestamp: int) -> str:
    """
    Converts a timestamp to a human readable format.

    Args:
        timestamp: The timestamp to convert.

    Returns:
        A human readable timestamp.
    """
    return datetime.utcfromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")


def preprocess_market_chart_to_dataframe(api_response: requests.models.Response) -> pd.DataFrame:
    """
    Preprocesses the market chart data from the API response.

    Args:
        api_response: The response from the API.

    Returns:
        A pandas dataframe with the market chart data.
    """
    data = api_response.json()
    if "error" not in data:
        dataframe = pd.DataFrame(data["prices"], columns=["timestamps", "prices"])
        dataframe["market_caps"] = [value[1] for value in data["market_caps"]]
        dataframe["total_volumes"] = [value[1] for value in data["total_volumes"]]
        dataframe["timestamps"] = dataframe["timestamps"].map(convert_timestamp)
        dataframe.dropna(inplace=True)
    return dataframe
