## Initialization

- `mkrich init [OPTIONS] SERVICE`

```bash
Command line interface for initializing a full project or a specific component.

- serving: initialize only the serving component, constisting of an API and a web server.

- interface: initialize only the interface component, constisting of a streamlit dashboard, a postgres database and a 
pgadmin UI.

- training: initialize only the training component, constisting of a training kedro pipeline and a fully prefect ETL 
pipeline.

Arguments:
  SERVICE  Service to initialize (interface, serving, training).  [required]

Options:
  -p, --path TEXT  Path to initialize, defaults to current directory
  --help           Show this message and exit.

```

- `mkrich run [OPTIONS] SERVICE`

```bash
Command line interface for running a specific component. You must have initialized the component before.

- interface: run the streamlit dashboard.

- serving: run the model serving API.

- training: run the Prefect ETL component that handles the training pipeline.

Arguments:
  SERVICE  Service you want to run (interface, serving or training). [required]


Options:
  --help  Show this message and exit.
```

- `mkrich start [OPTIONS] SERVICE`

```bash
Command line interface for starting a local agent that will do flows registered in the training component.

- agent: start the Prefect agent.

Arguments:
  SERVICE  Service you want to start (agent only for the moment).  [required]

Options:
  --help  Show this message and exit.
```

- `mkrich stop [OPTIONS]`

```bash
Command line interface for stopping all ressources deployed after `mkrich run training` command.

Options:
  --help  Show this message and exit.
```
