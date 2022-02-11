import pandas as pd

from typing import Dict

from make_us_rich.client import BinanceClient


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
    client = BinanceClient()
    data = client.get_data(symbol, parameters["interval"], parameters["start_date"])
    return data
