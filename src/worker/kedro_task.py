from datetime import timedelta

from prefect import Task

from kedro.io import DataCatalog
from kedro.pipeline.node import Node
from kedro.runner import run_node


class KedroTask(Task):
    """Kedro node as a Prefect task."""

    _max_retries = 5
    _retry_delay = timedelta(minutes=2)


    def __init__(self, node: Node, catalog: DataCatalog) -> None:
        self._node = node
        self._catalog = catalog
        super().__init__(
            name=node.name, 
            tags=node.tags,
            max_retries=self._max_retries,
            retry_delay=self._retry_delay
        )


    def run(self):
        """Run the node."""
        run_node(self._node, self._catalog)
