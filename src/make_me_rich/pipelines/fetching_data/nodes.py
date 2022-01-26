import pandas as pd

from binance.client import Client
from typing import Dict


def fetch_data_to_dataframe(
    currency: str, 
    compare: str,
    api_key: str,
    secret_key: str,
    parameters: Dict[str, str],
) -> pd.DataFrame:
    """
    Fetch data from the API and convert it to a pandas dataframe.

    Parameters
    ----------
    currency: str
        Currency to fetch data for.
    compare: str
        Currency to compare to.
    parameters: Dict[str, str]
        Dictionary of parameters.
    api_key: str
        API key for the Binance API.
    secret_key: str
        Secret key for the Binance API.
    
    Returns
    -------
    pd.DataFrame
        Pandas dataframe containing the data.
    """
    symbol = f"{currency.upper()}{compare.upper()}"
    binance_client = Client(api_key=api_key, api_secret=secret_key)
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
