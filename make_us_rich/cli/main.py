import git
import typer

from pathlib import Path, PurePath

from make_us_rich.utils import clean_dir

from . import ALL, INTERFACE, SERVING, TRAINING
from .runs_flavor import run_interface, run_serving, run_training


INIT_TYPES = ["full", "serving", "interface", "training"]
RUN_TYPES = ["serving", "training", "interface"]


app = typer.Typer()


@app.command("init")
def initialize(
    service: str = typer.Argument(..., help="Service to initialize (full, interface, serving, training)."),
    workdir: str = typer.Option(None, "--path", "-p", help="Path to initialize, defaults to current directory"),
):
    """
    Command line interface for initializing a full project or a specific component.

    - full: initialize the whole project on the same machine.

    - serving: initialize only the serving component, constisting of an API and a web server.

    - interface: initialize only the interface component, constisting of a streamlit dashboard, a postgres database and a 
    pgadmin UI.

    - training: initialize only the training component, constisting of a training kedro pipeline and a fully prefect ETL 
    pipeline.
    """
    service = service.lower()
    if service not in INIT_TYPES:
        raise typer.BadParameter(f"{service} is not a valid service. Valid service to initialize are {INIT_TYPES}")
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

    if service == "interface":
        exceptions = ALL + INTERFACE
    elif service == "serving":
        exceptions = ALL + SERVING
    elif service == "training":
        exceptions = ALL + TRAINING
    else:
        exceptions = ALL + INTERFACE + SERVING + TRAINING
    
    typer.secho("🗑️ Cleaning up make-us-rich useless files...\n", fg=typer.colors.YELLOW)
    clean_dir(workdir, exceptions)

    typer.secho(f"Setup complete! You can now run `mkrich run -h` to get help to start.\n", fg=typer.colors.GREEN)


@app.command("run")
def run(
    service: str = typer.Argument(..., help="Service you want to run (interface, serving or training).")
):
    """"""
    service = service.lower()
    if service not in RUN_TYPES:
        raise typer.BadParameter(f"{service} is not a valid service. Valid service to run are {RUN_TYPES}")
    current_directory = Path.cwd()
    if current_directory.name != f"mkrich-{service}":
        raise FileNotFoundError(
            f"You are not in the right working directory. Consider moving to mkrich-{service}."
        )
    typer.secho(f"🔄 Running {service}\n", fg=typer.colors.GREEN)

    if service == "interface":
        run_interface()
    elif service == "serving":
        run_serving()
    else:
        run_training()
