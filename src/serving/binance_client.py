import os
import pandas as pd

from binance.client import Client
from dotenv import load_dotenv


load_dotenv()


class BinanceClient:

    def __init__(self):
        self.client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_SECRET_KEY"))
        self.columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time", 
            "quote_av", "trades", "tb_base_av", "tb_quote_av", "ignore"]

    
    def get_five_days_data(self, symbol: str) -> pd.DataFrame:
        """
        Gets the data for the last five days.

        Parameters
        ----------
        symbol: str
            Symbol to get the data for.
        
        Returns
        -------
        pd.DataFrame
            Dataframe for the last five days.
        """
        symbol = symbol.upper()
        klines = self.client.get_historical_klines(symbol, "1h", "5 day ago UTC")
        data = pd.DataFrame(klines, columns=self.columns)
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
        return data

    
    def get_one_year_data(self, symbol: str) -> pd.DataFrame:
        """
        Gets the data for the last year.

        Parameters
        ----------
        symbol: str
            Symbol to get the data for.
        
        Returns
        -------
        pd.DataFrame
            Dataframe for the last year.
        """
        klines = self.client.get_historical_klines(symbol, "1h", "1 year ago UTC")
        data = pd.DataFrame(klines, columns=self.columns)
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
        return data