import argparse
import json
import logging
import os

from azureml.core import Dataset, Experiment
from azureml.train.automl import AutoMLConfig

from aml_utils import add_workspace_args, get_workspace

DATA_URL = (
    "https://automlsamplenotebookdata.blob.core.windows.net/"
    "automl-sample-notebook-data/bankmarketing_train.csv"
)


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--experiment-name", default="bankmarketing-automl")
    parser.add_argument("--dataset-name", default="Bankmarketing")
    parser.add_argument("--compute-target", required=True)
    parser.add_argument("--model-name", default="bankmarketing-automl-model")
    parser.add_argument("--max-concurrent-iterations", type=int, default=4)
    parser.add_argument("--experiment-timeout-mins", type=int, default=30)
    args = parser.parse_args()

    ws = get_workspace(args)
    experiment = Experiment(workspace=ws, name=args.experiment_name)

    dataset = Dataset.Tabular.from_delimited_files(path=DATA_URL)
    dataset = dataset.register(
        workspace=ws,
        name=args.dataset_name,
        create_new_version=True,
        description="Bank marketing training data",
    )

    automl_settings = {
        "task": "classification",
        "primary_metric": "AUC_weighted",
        "training_data": dataset,
        "label_column_name": "y",
        "n_cross_validations": 5,
        "enable_early_stopping": True,
        "experiment_timeout_minutes": args.experiment_timeout_mins,
        "max_concurrent_iterations": args.max_concurrent_iterations,
        "compute_target": args.compute_target,
        "featurization": "auto",
        "verbosity": logging.INFO,
    }

    automl_config = AutoMLConfig(**automl_settings)
    run = experiment.submit(automl_config, show_output=True)
    run.wait_for_completion(show_output=True)

    best_run, _ = run.get_output()
    registered_model = best_run.register_model(
        model_name=args.model_name,
        model_path="outputs/model.pkl",
        tags={"project": "bankmarketing-automl", "stage": "production-candidate"},
        description="Best model from AutoML classification run",
    )

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/best_run.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "automl_run_id": run.id,
                "best_child_run_id": best_run.id,
                "registered_model_name": registered_model.name,
                "registered_model_version": registered_model.version,
            },
            f,
            indent=2,
        )

    print("Saved best run metadata to artifacts/best_run.json")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
