from os import listdir
from os.path import isfile, isdir
from pathlib import Path
from shutil import rmtree
from typing import List, Union


def clean_dir(path_to_clean: Union[str, Path], exception: List[str]) -> None:
    """
    Removes all files and directories in the given path.

    Parameters
    ----------
    path_to_clean : Union[str, Path]
        Directory path to clean. If it is a string, it will be converted to a Path object.
    exception : List[str]
        List of files and directories to keep. If a file or directory is in this list, it will not be removed.
    """
    if isinstance(path_to_clean, str):
        path_to_clean = Path(path_to_clean)

    all_files = [f for f in listdir(path_to_clean) if isfile(path_to_clean.joinpath(f)) and f not in exception]
    for file in all_files:
        path_to_clean.joinpath(file).unlink()

    all_directories = [d for d in listdir(path_to_clean) if isdir(path_to_clean.joinpath(d)) and d not in exception]
    for directory in all_directories:
        rmtree(path_to_clean.joinpath(directory))
