import typer

from typing import List

from .runs_flavor import run_interface, run_serving, run_training
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
        List of exceptions.
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


def launch_service(service: str) -> bool:
    """
    Launch the service.

    Parameters
    ----------
    service: str
        Service to launch.

    Returns
    -------
    bool
        True if the service was launched, raises an error otherwise.
    """
    if service == "interface":
        run_interface()
    elif service == "serving":
        run_serving()
    elif service == "training":
        env_valid = ask_user_about_environment()
        if env_valid:
            run_training()
    else:
        raise typer.BadParameter(f"{service} is not a valid service. Valid service to run are {COMPONENTS}")
    return True


def ask_user_about_environment() -> bool:
    """
    """
    question = "Are you in the right environment?\nWe are going to install some required dependencies."
    typer.confirm(question, abort=True)
    return True