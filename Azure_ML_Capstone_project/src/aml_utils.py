import argparse
import json
import os
from pathlib import Path

from azureml.core import Dataset, Workspace
from azureml.core.authentication import (
    AzureCliAuthentication,
    InteractiveLoginAuthentication,
    ServicePrincipalAuthentication,
)


def _build_auth_from_env():
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")

    if tenant_id and client_id and client_secret:
        return ServicePrincipalAuthentication(
            tenant_id=tenant_id,
            service_principal_id=client_id,
            service_principal_password=client_secret,
        )

    try:
        return AzureCliAuthentication()
    except Exception:
        return InteractiveLoginAuthentication(tenant_id=tenant_id)


def get_workspace(config_path=None):
    if config_path and Path(config_path).exists():
        return Workspace.from_config(path=config_path, auth=_build_auth_from_env())

    raise ValueError(
        "Provide config file or set AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET"
    )


def add_workspace_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--config",
        default="config/aml_config.capstone.json",
        help="Path to Azure ML workspace config.json",
    )
