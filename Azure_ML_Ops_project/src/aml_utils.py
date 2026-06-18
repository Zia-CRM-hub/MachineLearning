import argparse
import os
from pathlib import Path

from azureml.core import Workspace
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


def get_workspace(args):
    if args.config and Path(args.config).exists():
        return Workspace.from_config(path=args.config, auth=_build_auth_from_env())

    required = [args.subscription_id, args.resource_group, args.workspace_name]
    if not all(required):
        raise ValueError(
            "Provide either --config with Azure ML config.json or all of "
            "--subscription-id, --resource-group, and --workspace-name"
        )

    return Workspace.get(
        name=args.workspace_name,
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        auth=_build_auth_from_env(),
    )


def add_workspace_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to Azure ML workspace config.json (default: config.json)",
    )
    parser.add_argument("--subscription-id", default=None, help="Azure subscription ID")
    parser.add_argument("--resource-group", default=None, help="Azure resource group")
    parser.add_argument("--workspace-name", default=None, help="Azure ML workspace name")
