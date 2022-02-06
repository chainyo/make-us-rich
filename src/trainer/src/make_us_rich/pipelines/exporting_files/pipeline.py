from kedro.pipeline import Pipeline, node

from .nodes import upload_files, clean_files


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=upload_files,
                inputs=[
                    "params:currency",
                    "params:compare",
                    "params:dir_path",
                    "validation_done",
                ],
                outputs="upload_done",
                name="uploading_files_node"
            ),
            node(
                func=clean_files,
                inputs=["upload_done"],
                outputs="clean_done",
                name="cleaning_files_node"
            ),
        ]
    )
