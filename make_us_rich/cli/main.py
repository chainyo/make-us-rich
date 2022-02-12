import git
import typer

from pathlib import Path

from make_us_rich.utils import clean_dir

from . import ALL, INTERFACE, SERVING, TRAINING


DEPLOY_TYPES = ["full", "serving", "interface", "training"]


app = typer.Typer()


@app.command("init")
def initialize(
    type: str = typer.Argument(..., help="Type of component to initialize (full, serving, interface, training)"),
    workdir: str = typer.Option(None, "--path", "-p", help="Path to deploy, defaults to current directory"),
):
    """
    Command line interface for deploying a full project or a specific component.

    - full: deploys the whole project on the same machine.

    - serving: deploys only the serving component, constisting of an API and a web server.

    - interface: deploys only the interface component, constisting of a streamlit dashboard, a postgres database and a 
    pgadmin UI.

    - training: deploys only the training component, constisting of a training kedro pipeline and a fully prefect ETL 
    pipeline.
    """
    if type not in DEPLOY_TYPES:
        raise typer.BadParameter(f"{type} is not a valid deploy type. Valid deploy types are {DEPLOY_TYPES}")
    typer.secho(f"🛠️ Initializing {type}", fg=typer.colors.GREEN)

    if workdir is None:
        workdir = Path.cwd()
    else:
        workdir = Path(workdir)
    workdir = workdir.joinpath(f"mkrich-{type}")
    if workdir.exists():
        raise typer.BadParameter(
            f"{workdir} already exists."
            f"\n\nPlease remove it or use a different path."
        )
    typer.secho(f"📁 Working directory: {workdir}")

    typer.secho(f"Recuperating make-us-rich {type} files...", fg=typer.colors.YELLOW)
    git.Repo.clone_from(url="https://github.com/ChainYo/make-us-rich.git", to_path=workdir)

    if type == "interface":
        exceptions = ALL + INTERFACE
    elif type == "serving":
        exceptions = ALL + SERVING
    elif type == "training":
        exceptions = ALL + TRAINING
    else:
        exceptions = ALL + INTERFACE + SERVING + TRAINING
    
    typer.secho("🗑️ Cleaning up make-us-rich useless files...", fg=typer.colors.MAGENTA)
    clean_dir(workdir, exceptions)

    typer.secho(f"Setup complete! You can now run `mkrich {type}` to get started.", fg=typer.colors.BRIGHT_BLUE)


@app.command("run")
def run():
    pass
