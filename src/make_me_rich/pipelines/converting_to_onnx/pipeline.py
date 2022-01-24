from kedro.pipeline import Pipeline, node

from .nodes import convert_model


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=convert_model,
                inputs=[
                    "train_sequences",
                    "val_sequences",
                    "test_sequences",
                    "params:dir_path"
                ],
                outputs=None,
                name="converting_model_node"
            ),
        ]
    )
