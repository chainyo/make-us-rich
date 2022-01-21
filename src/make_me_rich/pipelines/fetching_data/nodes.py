import pandas as pd

from binance.client import Client


def fetch_data_to_dataframe(
    currency: str, 
    compare: str,
    kline_size: str = Client.KLINE_INTERVAL_1DAY,
    ) -> pd.DataFrame:
    """
    Fetch data from the API and convert it to a pandas dataframe.

    Args:
        api_response: The response from the API.

    Returns:
        A pandas dataframe with the market chart data.
    """
    symbol = f"{currency.upper()}{compare.upper()}"
    binance_client = Client(api_key="params:API_KEY", api_secret="params:SECRET_KEY")
    klines = binance_client.get_historical_klines(symbol, kline_size, "3650 days ago UTC")
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
