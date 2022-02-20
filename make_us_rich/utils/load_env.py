"""All utility functions for the make_us_rich project.
"""
from dotenv import dotenv_values
from pathlib import Path
from typing import Dict, Optional


CORRECT_WORKDIR = ["make_us_rich", "mkrich-interface", "mkrich-serving", "mkrich-training"]


def load_env(file_name: str, config_dir: Optional[str] = None) -> Dict:
    """
    Loads the environment variables from the specified .env file.
    You don't need to specify `.env-` prefix for the file name.
    e.g. `load_env("my_env")` will load `.env-my_env` file.

    You can also specify the directory where the .env file is located. You need to provide
    the full path to the directory.

    Parameters
    ----------
    file_name: str
        Name of the .env file.
    config_dir: str
        Full path to the config directory.
    """
    env_filename = f".env-{file_name}"

    if config_dir is not None:
        return dotenv_values(config_dir.joinpath(env_filename))
    else:
        workdir = Path.cwd()
        if workdir.parts[-1] not in CORRECT_WORKDIR:
            raise ValueError(
                "Your are trying to load the environment variables from the wrong directory. "
                "Please make sure you are inside one of the following directories: "
                f"{CORRECT_WORKDIR}, "
                "or provide the full path to the config directory by adding the `config_dir` parameter."
            )
        config_path = workdir.joinpath("conf")
        
        if config_path.joinpath("local", env_filename).exists():
            config_file = dotenv_values(config_path.joinpath("local", env_filename))
            return config_file
        
        config_path = config_path.joinpath("base")
        try:
            config_file = dotenv_values(config_path.joinpath(env_filename))
            return config_file
        except FileNotFoundError:
            raise FileNotFoundError(
                f"File {env_filename} not found in {config_path}."
                "Please make sure you have the correct .env file in the `conf/base` directory or "
                "`conf/local` directory."
            )
