from pathlib import Path
from shutil import rmtree
from typing import List, Union


def clean_dir(path_to_clean: Union[str, Path], exception: List[str]) -> None:
    """
    Removes all files and directories in the given path if they don't match the exception list.

    Parameters
    ----------
    path_to_clean : Union[str, Path]
        Directory path to clean. If it is a string, it will be converted to a Path object.
    exception : List[str]
        List of files and directories to keep. If a file or directory is in this list, it will not be removed.
    """
    if isinstance(path_to_clean, str):
        path_to_clean = Path(path_to_clean)

    items_to_remove = [item for item in path_to_clean.iterdir() if item.name not in exception]
    for item in items_to_remove:
        if item.is_dir():
            rmtree(item)
        else:
            item.unlink()
