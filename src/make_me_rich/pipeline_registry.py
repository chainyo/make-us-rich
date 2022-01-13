"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline
from make_me_rich.pipelines import data_processing as dp


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    data_processing_pipeline = dp.create_pipeline()
    return {
        "__default__": data_processing_pipeline,
        "data_processing": data_processing_pipeline,
    }
