from kedro.pipeline import Pipeline, node

from .nodes import convert_model, validate_model


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=convert_model,
                inputs=[
                    "train_sequences",
                    "val_sequences",
                    "test_sequences",
                    "params:conversion",
                    "params:dir_path",
                    "training_done"
                ],
                outputs="conversion_outputs",
                name="converting_model_node"
            ),
            node(
                func=validate_model,
                inputs=[
                    "params:dir_path",
                    "conversion_outputs",
                ],
                outputs="validation_done",
                name="validating_model_node"
            ),
        ]
    )
