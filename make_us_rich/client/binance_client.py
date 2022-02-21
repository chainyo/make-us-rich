import pandas as pd

from binance.client import Client
from os import getenv
from typing import Optional

from make_us_rich.utils import load_env


class BinanceClient:

    def __init__(self):
        """
        Initializes the client for connecting to the Binance API.
        """
        try:
            self._config = load_env("binance")
        except:
            self._config = {"API_KEY": getenv("API_KEY"), "SECRET_KEY": getenv("SECRET_KEY")}
        self.client = Client(self._config["API_KEY"], self._config["SECRET_KEY"])
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

    
    def get_data(self, symbol: str, interval: str, start_time: str, end_time: Optional[str] = None) -> pd.DataFrame:
        """
        Gets the data for the given symbol, interval, and time range.

        Parameters
        ----------
        symbol: str
            Symbol to get the data for.
        interval: str
            Interval to get the data for.
        start_time: str
            Start time of the data.
        end_time: Optional[str]
            End time of the data. 
        
        Returns
        -------
        pd.DataFrame
            Dataframe for the given symbol, interval, and time range.
        """
        klines = self.client.get_historical_klines(symbol, interval, start_time, end_time)
        data = pd.DataFrame(klines, columns=self.columns)
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
        return data
