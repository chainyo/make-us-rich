from kedro.pipeline import Pipeline, node

from .nodes import format_market_chart_to_dataframe


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=format_market_chart_to_dataframe,
                inputs="inputs_market_chart",
                outputs="fetched_market_chart",
                name="fetching_data_node",
            ),
        ]
    )
