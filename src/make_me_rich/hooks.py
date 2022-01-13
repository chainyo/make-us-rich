"""Project hooks."""
from itertools import product
from math import prod
from typing import Any, Dict, Iterable, Optional

from kedro.config import ConfigLoader
from kedro.extras.datasets.api import APIDataSet
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.versioning import Journal


class ProjectHooks:
    @hook_impl
    def register_config_loader(
        self, conf_paths: Iterable[str], env: str, extra_params: Dict[str, Any],
    ) -> ConfigLoader:
        return ConfigLoader(conf_paths)

    @hook_impl
    def register_catalog(
        self,
        catalog: Optional[Dict[str, Dict[str, Any]]],
        credentials: Dict[str, Dict[str, Any]],
        load_versions: Dict[str, str],
        save_version: str,
        journal: Journal,
    ) -> DataCatalog:
        return DataCatalog.from_config(
            catalog, credentials, load_versions, save_version, journal
        )


class APICatalogHooks:
    @hook_impl
    def after_catalog_created(
        self, 
        catalog: DataCatalog,
        conf_catalog: Dict[str, Any],
        conf_creds: Dict[str, Any],
        feed_dict: Dict[str, Any],
        save_version: str,
        load_versions: Dict[str, str],
        run_id: str,
    ) -> None:
        """
        This hook is called after the catalog is created. It creates one entry in the catalog per crypto currency
        listed in the config file.
        """
        api_datasets_to_create = feed_dict["params:currencies_datasets"]
        datasets = list(product(api_datasets_to_create["currencies"], api_datasets_to_create["compare"]))

        for dataset in datasets:
            new_entry = {
                f"{dataset[0]}_vs_{dataset[1]}_market_chart": APIDataSet(
                    url=f"https://api.coingecko.com/api/v3/coins/{dataset[0]}/market_chart?vs_currency={dataset[1]}&days=max&interval=daily"
                ),
            }
            catalog.add(new_entry, replace=True)
