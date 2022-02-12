from datetime import timedelta
from pathlib import Path
from typing import Dict

from prefect import Client, Flow
from prefect.schedules import IntervalSchedule
from prefect.utilities.exceptions import ClientError

from kedro.framework.project import pipelines
from kedro.framework.session import KedroSession
from kedro.io import MemoryDataSet

from make_us_rich.worker import KedroTask
from make_us_rich.worker.project_metadata import ProjectMetadata, bootstrap_project


class Trainer:

    TARGETED_COINS = ["btc", "eth", "chz"]
    
    def __init__(self) -> None:
        """
        Initialize all training flows from a Kedro project pipeline.
        """
        self.metadata = self._get_kedro_project_metadata()
        self.client = Client()
        self._initialize_project()
        self.schedule = IntervalSchedule(interval=timedelta(hours=1))
        self.registered_flows = self._build_flows()

    
    def __repr__(self) -> str:
        return f"Trainer(project_path={self.metadata.project_path})"

    
    def list_registered_flows(self) -> Dict[str, Flow]:
        """
        List registered flows.

        Returns
        -------
        Dict
            Registered flows.
        """
        return self.registered_flows
        

    def _build_flows(self) -> Dict[str, Flow]:
        """
        Create one flow for each currency and add it to available flows.

        Returns
        -------
        Dict
            Available flows.
        """
        registered_flows = {}
        for currency in self.TARGETED_COINS:
            registered_flows[currency] = self._build_one_flow(currency)
        return registered_flows


    def _build_one_flow(self, currency: str, compare: str = "usdt", register: bool = True) -> Flow:
        """
        Build a Prefect Flow from a Kedro project.

        Parameters
        ----------
        metadata: ProjectMetadata
            Metadata of the Kedro project.
        currency: str
            Currency used in the model.
        compare: str
            Compare used in the model. Default is "usdt".
        
        Returns
        -------
        Flow
            Prefect Flow built from the Kedro project.
        """
        session = KedroSession.create(
            project_path=self.metadata.project_path, extra_params={"currency": currency, "compare": compare}
        )
        context = session.load_context()
        catalog = context.catalog
        pipeline_name = "__default__"
        pipeline = pipelines.get(pipeline_name)
        unregistered_ds = pipeline.data_sets() - set(catalog.list())

        for ds_name in unregistered_ds:
            catalog.add(ds_name, MemoryDataSet())

        with Flow(f"{currency}_{compare}", self.schedule) as flow:
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

        if register:
            flow.register(self.metadata.project_name)

        return flow


    def _get_kedro_project_metadata(self) -> ProjectMetadata:
        """
        Get the metadata of a Kedro project.
        
        Returns
        -------
        dict
            Metadata of the Kedro project.
        """
        project_path = Path.cwd()
        metadata = bootstrap_project(project_path)
        return metadata


    def _initialize_project(self) -> None:
        """
        Initialize a Kedro project inside a Prefect Flow project.

        Parameters
        ----------
        project_name: str
            Name of the Prefect Flow project.
        """
        try:
            self.client.create_project(project_name=self.metadata.project_name)
        except ClientError:
            # `project_name` project already exists
            pass


if __name__ == "__main__":
    flow = Trainer()
    print(flow.list_registered_flows())
