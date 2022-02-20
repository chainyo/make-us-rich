import typer

from typing import List, Dict

from make_us_rich.utils import load_env
from . import (
    ALL, 
    COMPONENTS,
    INTERFACE, 
    SERVING, 
    TRAINING
)


def check_the_service(service: str) -> bool:
    """
    Check if the service exists.

    Parameters
    ----------
    service: str
        Service to check.
    
    Returns
    -------
    bool
        True if the service exists, raises an error otherwise.
    """
    if service not in COMPONENTS:
        raise typer.BadParameter(f"{service} is not a valid service. Valid service to run are {COMPONENTS}")
    else:
        return True


def get_exceptions(service: str) -> List:
    """
    Get the exceptions for the service.

    Parameters
    ----------
    service: str
        Service to check.
    
    Returns
    -------
    List
        List of exceptions, raises an error otherwise.
    """
    if service == "interface":
        exceptions = ALL + INTERFACE
    elif service == "serving":
        exceptions = ALL + SERVING
    elif service == "training":
        exceptions = ALL + TRAINING
    else:
        raise typer.BadParameter(f"{service} is not a valid service. Valid service to run are {COMPONENTS}")
    return exceptions


def ask_user_about_environment() -> bool:
    """
    Ask the user if the right environment is active.

    Returns
    -------
    bool
        True if the environment is valid, raises an error otherwise.
    """
    question = "Are you in the right environment?\nWe are going to install some required dependencies."
    typer.confirm(question, abort=True)
    return True


def env_variables(files: List[str]) -> Dict[str, Dict]:
    """
    Get the environment variables from the listed files. It will raise an error if the file does not exist. It will
    also raise an error if env variables are not valid, e.g. if they are equal to `changeme`.

    Parameters
    ----------
    files: List[str]
        List of files to check.
    
    Returns
    -------
    Dict[str, Dict]
        Dictionary of environment variables.
    """
    config = {}
    for file in files:
        variables = load_env(file)

        for key, value in variables.items():
            if value == "changeme":
                raise typer.BadParameter(f"You need to set the {key} environment variable.")

        config[file] = variables

    return config
