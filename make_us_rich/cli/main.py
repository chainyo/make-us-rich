import git
import typer

from pathlib import Path

from make_us_rich.utils import clean_dir
from .runner import ComponentRunner
from .utils import (
    check_the_service, 
    get_exceptions, 
)


app = typer.Typer()
runner = ComponentRunner()


@app.command("init")
def initialize(
    service: str = typer.Argument(..., help="Service to initialize (interface, serving, training)."),
    workdir: str = typer.Option(None, "--path", "-p", help="Path to initialize, defaults to current directory"),
):
    """
    Command line interface for initializing a full project or a specific component.

    - serving: initialize only the serving component, constisting of an API and a web server.

    - interface: initialize only the interface component, constisting of a streamlit dashboard, a postgres database and a 
    pgadmin UI.

    - training: initialize only the training component, constisting of a training kedro pipeline and a fully prefect ETL 
    pipeline.
    """
    service = service.lower()
    check_the_service(service)
    typer.secho(f"🛠️ Initializing {service}\n", fg=typer.colors.GREEN)

    if workdir is None:
        workdir = Path.cwd()
    else:
        workdir = Path(workdir)
    workdir = workdir.joinpath(f"mkrich-{service}")
    
    if workdir.exists():
        raise typer.BadParameter(
            f"{workdir} already exists."
            f"\n\nPlease remove it or use a different path."
        )
    typer.echo(f"📁 Working directory: {workdir}")

    typer.echo(f"Recuperating make-us-rich {service} files...\n")
    git.Repo.clone_from(url="https://github.com/ChainYo/make-us-rich.git", to_path=workdir)

    typer.secho("🗑️ Cleaning up make-us-rich useless files...\n", fg=typer.colors.YELLOW)
    exceptions = get_exceptions(service)
    clean_dir(workdir, exceptions)

    typer.secho(f"Setup complete! You can now run `mkrich run --help` to get help to start.\n", fg=typer.colors.GREEN)


@app.command("run")
def run(
    service: str = typer.Argument(..., help="Service you want to run (interface, serving or training).")
):
    """
    Command line interface for running a specific component. You must have initialized the component before.

    - interface: run the streamlit dashboard.

    - serving: run the model serving API.

    - training: run the Prefect ETL component that handles the training pipeline.
    """
    service = service.lower()
    check_the_service(service)

    current_directory = Path.cwd()
    if current_directory.name != f"mkrich-{service}":
        raise FileNotFoundError(
            f"You are not in the right working directory. Consider moving to mkrich-{service}."
        )
    typer.secho(f"🔄 Running {service}\n", fg=typer.colors.GREEN)

    launched = runner(service)
    if launched:
        typer.secho(f"🚀 {service} is running!\n", fg=typer.colors.GREEN)
