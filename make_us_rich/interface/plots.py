import pandas as pd
import plotly.graph_objects as go

from datetime import timedelta
from typing import Any, Dict, Tuple


def candlestick_plot(data: pd.DataFrame, currency: str, compare: str, pred: float) -> go.Figure:
    """
    Create candlestick plot.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe containing the data to plot.
    currency : str
        Currency to plot.
    compare : str
        Currency to compare.
    pred : float
        Prediction to plot.
    
    Returns
    -------
    go.Figure
        Plotly figure.
    """
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=data["timestamp"], open=data["open"], high=data["high"], low=data["low"], close=data["close"], 
            name="Candlestick"
        )
    )
    fig.update_layout(
        title=f"{currency.upper()}/{compare.upper()} - last 5 days",
        yaxis_title=f"{currency.upper()} Price",
    )
    pred = float(data.iloc[-1]["close"]) + pred
    timestamp = data["timestamp"].max() + timedelta(hours=1)
    fig.add_trace(
        go.Scatter(
            x=[timestamp], y=[pred], mode="markers", marker_color="red", name="Prediction"
        )
    )
    fig.update_layout(
        title=f"{currency.upper()}/{compare.upper()} - last 5 days",
        yaxis_title=f"{currency.upper()} Price",
        annotations=[
            go.Annotation(
                x=timestamp,
                y=pred,
                text=f"Prediction: {pred:.3f}",
                showarrow=False,
            )
        ],
    )
    return fig


def scatter_plot(data: pd.DataFrame, currency: str, compare: str, pred: float) -> go.Figure:
    """
    Create scatter plot.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe containing the data to plot.
    currency : str
        Currency to plot.
    compare : str
        Currency to compare.
    pred : float
        Prediction to plot.
    
    Returns
    -------
    go.Figure
        Plotly figure.
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["timestamp"], y=data["close"], name="Close Price", line_color="blue", connectgaps=True
        )
    )
    fig.update_layout(
        title=f"{currency.upper()}/{compare.upper()} - last 5 days",
        yaxis_title=f"{currency.upper()} Price",
    )
    pred = float(data.iloc[-1]["close"]) + pred
    timestamp = data["timestamp"].max() + timedelta(hours=1)
    fig.add_trace(
        go.Scatter(
            x=[timestamp], y=[pred], mode="markers", marker_color="red", name="Prediction"
        )
    )
    fig.update_layout(
        title=f"{currency.upper()}/{compare.upper()} - last 5 days",
        yaxis_title=f"{currency.upper()} Price",
        annotations=[
            go.Annotation(
                x=timestamp,
                y=pred,
                text=f"Prediction: {pred:.3f}",
                showarrow=False,
            )
        ],
    )
    return fig


def format_data(data: Dict[str, Any]) -> Tuple[pd.DataFrame, float]:
    """
    Format data from API response before plotting.

    Parameters
    ----------
    data : Dict[str, Any]
        Data from API response.
    
    Returns
    -------
    Tuple[pd.DataFrame, float]
        Dataframe containing the data to plot and the prediction.
    """
    pred = data["prediction"]
    df = pd.DataFrame(
        data=data["data"],
        columns=[
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
            "ignore",
        ],
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["close"] = pd.to_numeric(df["close"], downcast="float")
    df["open"] = pd.to_numeric(df["open"], downcast="float")
    df["high"] = pd.to_numeric(df["high"], downcast="float")
    df["low"] = pd.to_numeric(df["low"], downcast="float")
    return df, pred