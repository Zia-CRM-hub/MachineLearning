import argparse
import json
import os

from azureml.core import Environment, Model
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice

from aml_utils import add_workspace_args, get_workspace


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--endpoint-name", default="capstone-endpoint")
    parser.add_argument("--cpu-cores", type=float, default=1.0)
    parser.add_argument("--memory-gb", type=float, default=2.0)
    args = parser.parse_args()

    ws = get_workspace(args.config)

    # Get model
    model = Model(ws, name=args.model_name)

    # Create environment
    env = Environment(name="capstone-inference-env")
    conda = CondaDependencies()
    conda.add_conda_package("python=3.10")
    conda.add_pip_package("azureml-defaults==1.62.0")
    conda.add_pip_package("joblib==1.4.2")
    conda.add_pip_package("pandas==2.2.2")
    conda.add_pip_package("scikit-learn==1.5.1")
    env.python.conda_dependencies = conda

    # Inference config
    inference_config = InferenceConfig(entry_script="src/score.py", environment=env)

    # Deployment config
    deployment_config = AciWebservice.deploy_configuration(
        cpu_cores=args.cpu_cores,
        memory_gb=args.memory_gb,
        auth_enabled=True,
        enable_app_insights=True,
    )

    # Deploy
    service = Model.deploy(
        workspace=ws,
        name=args.endpoint_name,
        models=[model],
        inference_config=inference_config,
        deployment_config=deployment_config,
        overwrite=True,
    )
    service.wait_for_deployment(show_output=True)

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/deployment_details.json", "w") as f:
        json.dump(
            {
                "service_name": service.name,
                "state": service.state,
                "scoring_uri": service.scoring_uri,
                "swagger_uri": service.swagger_uri,
                "app_insights_enabled": service.properties.get(
                    "AppInsightsEnabled", "unknown"
                ),
            },
            f,
            indent=2,
        )

    print(f"Deployment complete. Service URL: {service.scoring_uri}")


if __name__ == "__main__":
    main()
