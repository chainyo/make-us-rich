import pandas as pd

from binance.client import Client
from typing import Dict


def fetch_data_to_dataframe(
    currency: str, 
    compare: str,
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
    
    Returns
    -------
    pd.DataFrame
        Pandas dataframe containing the data.
    """
    symbol = f"{currency.upper()}{compare.upper()}"
    binance_client = Client(
        api_key="params:BINANCE_API_KEY", api_secret="params:BINANCE_SECRET_KEY"
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
