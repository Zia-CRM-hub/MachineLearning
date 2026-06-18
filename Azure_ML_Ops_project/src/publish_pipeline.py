import argparse
import json
import os

from azureml.core import Dataset, Environment, Experiment
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.compute_target import ComputeTargetException
from azureml.core.conda_dependencies import CondaDependencies
from azureml.pipeline.core import Pipeline
from azureml.pipeline.core.pipeline_endpoint import PipelineEndpoint
from azureml.pipeline.core.pipeline_data import PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.runconfig import RunConfiguration

from aml_utils import add_workspace_args, get_workspace

DATA_URL = (
    "https://automlsamplenotebookdata.blob.core.windows.net/"
    "automl-sample-notebook-data/bankmarketing_train.csv"
)


def get_or_create_compute(ws, compute_name, vm_size, max_nodes):
    try:
        return ComputeTarget(workspace=ws, name=compute_name)
    except ComputeTargetException:
        config = AmlCompute.provisioning_configuration(
            vm_size=vm_size,
            min_nodes=0,
            max_nodes=max_nodes,
        )
        target = ComputeTarget.create(ws, compute_name, config)
        target.wait_for_completion(show_output=True)
        return target


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--pipeline-experiment-name", default="pipeline-rest-endpoint")
    parser.add_argument("--pipeline-name", default="bankmarketing-training-pipeline")
    parser.add_argument("--pipeline-endpoint-name", default="bankmarketing-pipeline-endpoint")
    parser.add_argument("--compute-name", default="cpu-cluster")
    parser.add_argument("--vm-size", default="STANDARD_DS3_V2")
    parser.add_argument("--max-nodes", type=int, default=4)
    parser.add_argument("--dataset-name", default="Bankmarketing")
    args = parser.parse_args()

    ws = get_workspace(args)
    compute = get_or_create_compute(ws, args.compute_name, args.vm_size, args.max_nodes)

    dataset = Dataset.Tabular.from_delimited_files(path=DATA_URL)
    dataset = dataset.register(
        workspace=ws,
        name=args.dataset_name,
        create_new_version=True,
        description="Bank marketing training data for pipeline",
    )

    dataset_input = dataset.as_named_input("bankmarketing").as_download()
    model_output = PipelineData("model_output", datastore=ws.get_default_datastore())

    env = Environment(name="bankmarketing-pipeline-env")
    deps = CondaDependencies()
    deps.add_conda_package("python=3.10")
    deps.add_pip_package("pandas==2.2.2")
    deps.add_pip_package("scikit-learn==1.5.1")
    deps.add_pip_package("joblib==1.4.2")
    env.python.conda_dependencies = deps

    run_config = RunConfiguration()
    run_config.environment = env

    train_step = PythonScriptStep(
        name="Train Logistic Regression Model",
        script_name="train_pipeline_model.py",
        source_directory="src",
        arguments=["--bankmarketing", dataset_input, "--model-output", model_output],
        inputs=[dataset_input],
        outputs=[model_output],
        compute_target=compute,
        runconfig=run_config,
        allow_reuse=False,
    )

    pipeline = Pipeline(workspace=ws, steps=[train_step])
    pipeline.validate()

    experiment = Experiment(workspace=ws, name=args.pipeline_experiment_name)
    pipeline_run = experiment.submit(pipeline)
    pipeline_run.wait_for_completion(show_output=True)

    published = pipeline.publish(
        name=args.pipeline_name,
        description="Bank marketing training pipeline",
        version="1.0",
    )

    pipeline_endpoint = PipelineEndpoint.publish(
        workspace=ws,
        name=args.pipeline_endpoint_name,
        pipeline=published,
        description="REST endpoint for bank marketing pipeline",
    )

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/published_pipeline.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "pipeline_id": published.id,
                "pipeline_name": published.name,
                "published_endpoint": published.endpoint,
                "pipeline_endpoint_name": pipeline_endpoint.name,
                "pipeline_endpoint_id": pipeline_endpoint.id,
                "pipeline_endpoint_url": pipeline_endpoint.endpoint,
                "experiment_name": args.pipeline_experiment_name,
                "pipeline_run_id": pipeline_run.id,
            },
            f,
            indent=2,
        )

    print("Pipeline published.")
    print("Published pipeline endpoint:", published.endpoint)
    print("Pipeline endpoint URL:", pipeline_endpoint.endpoint)
    print("Saved pipeline metadata to artifacts/published_pipeline.json")


if __name__ == "__main__":
    main()
