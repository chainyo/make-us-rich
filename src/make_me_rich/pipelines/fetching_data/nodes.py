import pandas as pd

from binance.client import Client
from typing import Dict


def fetch_data_to_dataframe(
    currency: str, 
    compare: str,
    parameters: Dict[str, str],
    credentials: Dict[str, str],
) -> pd.DataFrame:
    """
    Fetch data from the API and convert it to a pandas dataframe.

    Args:
        currency: The currency to fetch data for.
        compare: The currency to compare to.
        parameters: The parameters to use for the API call.
        credentials: The credentials to use for the API call.

    Returns:
        A pandas dataframe with the market chart data.
    """
    symbol = f"{currency.upper()}{compare.upper()}"
    binance_client = Client(
        api_key=credentials["API_KEY"], api_secret=credentials["SECRET_KEY"]
    )
    klines = binance_client.get_historical_klines(
        symbol, parameters["interval"], parameters["start_date"]
    )
    data = pd.DataFrame(
        klines, 
        columns = [
            "timestamp", 
            "open", 
            "high", 
            "low", 
            "close", 
            "volume", 
            "close_time", 
            "quote_av", 
            "trades", 
            "tb_base_av", 
            "tb_quote_av", 
            "ignore"
        ],
    )
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
    return data
