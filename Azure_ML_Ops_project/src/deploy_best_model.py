import argparse
import json
import os

from azureml.core import Environment, Model
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice

from aml_utils import add_workspace_args, get_workspace


def resolve_model(ws, model_name, model_version=None):
    if model_version:
        return Model(workspace=ws, name=model_name, version=model_version)

    matches = [m for m in Model.list(ws, name=model_name)]
    if not matches:
        raise ValueError(f"No registered model found with name: {model_name}")
    return sorted(matches, key=lambda m: m.version, reverse=True)[0]


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--model-name", default="bankmarketing-automl-model")
    parser.add_argument("--model-version", type=int, default=None)
    parser.add_argument("--service-name", default="bankmarketing-service")
    parser.add_argument("--cpu-cores", type=float, default=1.0)
    parser.add_argument("--memory-gb", type=float, default=2.0)
    args = parser.parse_args()

    ws = get_workspace(args)
    model = resolve_model(ws, args.model_name, args.model_version)

    env = Environment(name="bankmarketing-inference-env")
    conda = CondaDependencies()
    conda.add_conda_package("python=3.10")
    conda.add_pip_package("azureml-defaults==1.62.0")
    conda.add_pip_package("joblib==1.4.2")
    conda.add_pip_package("pandas==2.2.2")
    conda.add_pip_package("scikit-learn==1.5.1")
    env.python.conda_dependencies = conda

    inference_config = InferenceConfig(entry_script="src/score.py", environment=env)

    deployment_config = AciWebservice.deploy_configuration(
        cpu_cores=args.cpu_cores,
        memory_gb=args.memory_gb,
        auth_enabled=True,
        enable_app_insights=True,
    )

    service = Model.deploy(
        workspace=ws,
        name=args.service_name,
        models=[model],
        inference_config=inference_config,
        deployment_config=deployment_config,
        overwrite=True,
    )
    service.wait_for_deployment(show_output=True)

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/service_details.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "service_name": service.name,
                "state": service.state,
                "scoring_uri": service.scoring_uri,
                "swagger_uri": service.swagger_uri,
                "model_name": model.name,
                "model_version": model.version,
            },
            f,
            indent=2,
        )

    print("Saved deployment metadata to artifacts/service_details.json")


if __name__ == "__main__":
    main()
