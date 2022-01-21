from kedro.pipeline import Pipeline, node

from .nodes import fetch_data_to_dataframe


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=fetch_data_to_dataframe,
                inputs=["params:currency", "params:compare"],
                outputs="fetched_market_chart",
                name="fetching_data_node",
            ),
        ]
    )
