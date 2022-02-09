# <project_root>/register_prefect_flow.py
from pathlib import Path

import click

from prefect import Client, Flow, Task
from prefect.utilities.exceptions import ClientError

from kedro.framework.project import pipelines
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from kedro.io import DataCatalog, MemoryDataSet
from kedro.pipeline.node import Node
from kedro.runner import run_node


class KedroTask(Task):
    """Kedro node as a Prefect task."""

    def __init__(self, node: Node, catalog: DataCatalog) -> None:
        self._node = node
        self._catalog = catalog
        super().__init__(name=node.name, tags=node.tags)

    def run(self):
        run_node(self._node, self._catalog)


@click.command()
@click.option("-p", "--pipeline", "pipeline_name", default=None)
@click.option("--env", "-e", type=str, default=None)
def build_and_register_flow(pipeline_name, env):
    """Register a Kedro pipeline as a Prefect flow."""
    project_path = Path.cwd()
    metadata = bootstrap_project(project_path)

    session = KedroSession.create(project_path=project_path, env=env)
    context = session.load_context()

    catalog = context.catalog
    pipeline_name = pipeline_name or "__default__"
    pipeline = pipelines.get(pipeline_name)

    unregistered_ds = pipeline.data_sets() - set(catalog.list())
    for ds_name in unregistered_ds:
        catalog.add(ds_name, MemoryDataSet())

    flow = Flow(metadata.project_name)

    tasks = {}
    for node, parent_nodes in pipeline.node_dependencies.items():
        if node._unique_key not in tasks:
            node_task = KedroTask(node, catalog)
            tasks[node._unique_key] = node_task
        else:
            node_task = tasks[node._unique_key]

        parent_tasks = []

        for parent in parent_nodes:
            if parent._unique_key not in tasks:
                parent_task = KedroTask(parent, catalog)
                tasks[parent._unique_key] = parent_task
            else:
                parent_task = tasks[parent._unique_key]

            parent_tasks.append(parent_task)

        flow.set_dependencies(task=node_task, upstream_tasks=parent_tasks)

    client = Client()
    try:
        client.create_project(project_name=metadata.project_name)
    except ClientError:
        # `metadata.project_name` project already exists
        pass

    # Register the flow with the server
    flow.register(project_name=metadata.project_name)

    # Start a local agent that can communicate between the server
    # and your flow code
    flow.run_agent()


if __name__ == "__main__":
    build_and_register_flow()
