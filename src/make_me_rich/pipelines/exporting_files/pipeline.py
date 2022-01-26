from kedro.pipeline import Pipeline, node

from .nodes import upload_files


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=upload_files,
                inputs=["params:MINIO"],
                outputs="conversion_outputs",
                name="converting_model_node"
            ),
        ]
    )
