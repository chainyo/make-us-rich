import docker
import typer

from . import COMPONENTS
from .utils import ask_user_about_environment, env_variables


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

    
    def _run_interface(self) -> bool:
        """
        Run the interface.

        Returns
        -------
        bool
            True if the service exists, raises an error otherwise.
        """
        typer.echo("Pulling images needed for the interface\n")
        self.client.images.pull("postgres", tag="13.4")
        self.client.images.pull("dpage/pgadmin4", tag="snapshot")
        
        typer.echo("Checking env variables\n")
        config = env_variables(["pgadmin", "postgres", "api"])

        typer.echo("Building postgres database\n")
        self.client.containers.run(
            "postgres", name="postgres", restart_policy={"Name": "unless-stopped"},
            environment=config["postgres"], ports={5432: 5432}, detach=True,
            volumes={
                "./database/init.sql": {"bind": "/docker-entrypoint-initdb.d/init.sql", "mode": "rw"},
                "./database/postgres-data": {"bind": "/var/lib/postgresql/data", "mode": "rw"},
            },
        )
        typer.echo("Building pgadmin\n")

        self.client.containers.run(
            "dpage/pgadmin4", name="pgadmin", restart_policy={"Name": "unless-stopped"},
            environment=config["pgadmin"], ports={5050: 80}, detach=True,
            volumes={"pgadmin-data": {"bind": "/var/lib/pgadmin", "mode": "rw"}},
        )
        typer.echo("Building interface\n")

        self.client.images.build(fileobj="Dockerfile", tag="mkrich-interface:latest")
        config_for_interface = config["postgres"] + config["api"]
        self.client.containers.run(
            "mkrich-interface:latest", name="interface", restart_policy={"Name": "unless-stopped"},
            environment=config_for_interface, ports={8501: 8501}, detach=True,
        )
        
        return True

    def _run_serving(self):
        """"""
        print("Running serving")


    def _run_training(self):
        """"""
        print("Running training")
