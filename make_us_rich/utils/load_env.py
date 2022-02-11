"""All utility functions for the make_us_rich project.
"""
import os 

from dotenv import dotenv_values
from pathlib import Path
from typing import Dict, Optional


def load_env(file_name: str, config_dir: Optional[str] = None) -> Dict:
    """
    Loads the environment variables from the specified .env file.
    You don't need to specify `.env-` prefix for the file name.
    e.g. `load_env("my_env")` will load `.env-my_env` file.

    Parameters
    ----------
    file_name: str
        Name of the .env file.
    config_dir: str
        Subdirectory of the project conf directory where the .env file is located.
    """
    workdir = Path.cwd()
    if workdir.parts[-1] != "make-us-rich":
        raise ValueError("Please run the script from the make-us-rich root directory.")
    config_path = workdir.joinpath("conf")
    env_filename = f".env-{file_name}"
    
    if config_dir is not None:
        config_file = dotenv_values(config_path.joinpath(config_dir, env_filename))
        return config_file
    
    if config_path.joinpath("local", env_filename).exists():
        config_file = dotenv_values(config_path.joinpath("local", env_filename))
        return config_file
    
    config_path = config_path.joinpath("base")
    try:
        config_file = dotenv_values(config_path.joinpath(env_filename))
        return config_file
    except FileNotFoundError:
        raise FileNotFoundError(f"File {env_filename} not found in {config_path}.")
