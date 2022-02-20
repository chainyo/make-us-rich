import docker
import typer

from . import COMPONENTS
from .utils import ask_user_about_environment


class ComponentRunner:
    """This class is used to run the components of the project by the cli."""
    def __init__(self) -> None:
        """
        Initialize the Runner class that will run the components.
        """
        self.client = docker.from_env()
        self.available_services = COMPONENTS

    
    def __call__(self, service: str):
        """
        Call the run function.

        Parameters
        ----------
        service: str
            Service to run.
        """
        return self.run(service)

    
    def run(self, service: str) -> bool:
        """
        Function that will run the service passed as argument.

        Parameters
        ----------
        service: str
            Service to run.
        
        Returns
        -------
        bool
            True if the service exists, raises an error otherwise.
        """
        self._check_service(service)
        
        if service == "interface":
            self._run_interface()
        elif service == "serving":
            self._run_serving()
        elif service == "training":
            ask_user_about_environment()
            self._run_training()
        return True

    
    def _check_service(self, service: str) -> bool:
        """
        Check if the service exists in the available services.

        Parameters
        ----------
        service: str
            Service to check.
        
        Returns
        -------
        bool
            True if the service exists, raises an error otherwise.
        """
        if service not in self.available_services:
            raise typer.BadParameter(f"{service} is not a valid service. Valid service to run are {COMPONENTS}")
        return True

    
    def _run_interface(self):
        """"""
        print("Running interface")


    def _run_serving(self):
        """"""
        print("Running serving")


    def _run_training(self):
        """"""
        print("Running training")
