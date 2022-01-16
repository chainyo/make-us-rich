from kedro.pipeline import Pipeline, node

from .nodes import


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=,
                inputs="preprocessed_market_chart",
                outputs=,
                name="training_data_node",
            ),
        ]
    )
