"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline
from make_me_rich.pipelines import fetching_data as fd
from make_me_rich.pipelines import preprocessing_data as pd
from make_me_rich.pipelines import training_model as tm


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    fetching_data_pipeline = fd.create_pipeline()
    preprocessing_data_pipeline = pd.create_pipeline()
    training_model_pipeline = tm.create_pipeline()
    return {
        "__default__": fetching_data_pipeline + preprocessing_data_pipeline + training_model_pipeline,
        "fetching_data": fetching_data_pipeline,
        "preprocessing_data": preprocessing_data_pipeline,
        "training_model": training_model_pipeline,
    }
