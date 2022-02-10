"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from make_us_rich.pipelines import fetching as fd
from make_us_rich.pipelines import preprocessing as pd
from make_us_rich.pipelines import training as tm
from make_us_rich.pipelines import converting as cto
from make_us_rich.pipelines import exporting as uf


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    fetching_pipeline = fd.create_pipeline()
    preprocessing_pipeline = pd.create_pipeline()
    training_pipeline = tm.create_pipeline()
    converting_pipeline = cto.create_pipeline()
    uploading_files_pipeline = uf.create_pipeline()
    return {
        "__default__": fetching_pipeline + preprocessing_pipeline + training_pipeline + converting_pipeline + uploading_files_pipeline,
        "fetching": fetching_pipeline,
        "preprocessing": preprocessing_pipeline,
        "training": training_pipeline,
        "converting": converting_pipeline,
        "uploading_files": uploading_files_pipeline,
    }
