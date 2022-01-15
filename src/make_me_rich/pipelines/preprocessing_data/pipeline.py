from kedro.pipeline import Pipeline, node

from .nodes import format_market_chart_to_dataframe


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=format_market_chart_to_dataframe,
                inputs="fetched_market_chart",
                outputs="preprocessed_market_chart",
                name="preprocessing_data_node",
            ),
        ]
    )
