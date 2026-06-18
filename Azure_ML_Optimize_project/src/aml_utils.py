"""
Azure ML Utilities for Optimize Project

Provides workspace authentication, configuration loading, and common utility functions.
"""

import os
import json
from pathlib import Path
from azureml.core.authentication import (
    InteractiveLoginAuthentication,
    AzureCliAuthentication,
    ServicePrincipalAuthentication
)
from azureml.core import Workspace


def _build_auth_from_env():
    """
    Build authentication object from environment variables.
    
    Tries service principal first, then falls back to Azure CLI authentication.
    """
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    
    if tenant_id and client_id and client_secret:
        return ServicePrincipalAuthentication(
            tenant_id=tenant_id,
            service_principal_id=client_id,
            service_principal_password=client_secret
        )
    
    try:
        return AzureCliAuthentication()
    except Exception:
        return InteractiveLoginAuthentication()


def get_workspace(config_path: str = None) -> Workspace:
    """
    Get Azure ML workspace from config or environment.
    
    Args:
        config_path: Path to aml_config.optimize.json
        
    Returns:
        Workspace object
    """
    if config_path and Path(config_path).exists():
        return Workspace.from_config(path=config_path)
    
    auth = _build_auth_from_env()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    workspace_name = os.getenv("AZURE_ML_WORKSPACE")
    
    return Workspace(
        subscription_id=subscription_id,
        resource_group=resource_group,
        workspace_name=workspace_name,
        auth=auth
    )


def load_config(config_path: str) -> dict:
    """Load JSON configuration file."""
    with open(config_path) as f:
        return json.load(f)


def add_workspace_args(parser):
    """Add common workspace arguments to argument parser."""
    parser.add_argument(
        "--config",
        type=str,
        default="config/aml_config.optimize.json",
        help="Path to Azure ML workspace config"
    )
    parser.add_argument(
        "--compute-target",
        type=str,
        default="optimize-compute",
        help="Azure ML compute cluster name"
    )
