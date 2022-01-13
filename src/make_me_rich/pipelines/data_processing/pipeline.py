from kedro.pipeline import Pipeline, node

from .nodes import preprocess_market_chart_to_dataframe


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=preprocess_market_chart_to_dataframe,
                inputs="bitcoin_vs_usd_market_chart",
                outputs="preprocessed_bitcoin_vs_usd_market_chart",
                name="preprocess_bitcoin_node",
            ),
            node (
                func=preprocess_market_chart_to_dataframe,
                inputs="chiliz_vs_usd_market_chart",
                outputs="preprocessed_chiliz_vs_usd_market_chart",
                name="preprocess_chiliz_node",
            ),
            node(
                func=preprocess_market_chart_to_dataframe,
                inputs="eos_vs_usd_market_chart",
                outputs="preprocessed_eos_vs_usd_market_chart",
                name="preprocess_eos_node",
            ),
            node(
                func=preprocess_market_chart_to_dataframe,
                inputs="ethereum_vs_usd_market_chart",
                outputs="preprocessed_ethereum_vs_usd_market_chart",
                name="preprocess_ethereum_node",
            ),
            node(
                func=preprocess_market_chart_to_dataframe,
                inputs="ripple_vs_usd_market_chart",
                outputs="preprocessed_ripple_vs_usd_market_chart",
                name="preprocess_ripple_node",
            ),
        ]
    )
