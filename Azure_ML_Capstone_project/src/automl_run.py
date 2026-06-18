import argparse
import json
import logging
import os

from azureml.core import Dataset, Experiment
from azureml.train.automl import AutoMLConfig

from aml_utils import add_workspace_args, get_workspace


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--experiment-name", default="capstone-automl")
    parser.add_argument("--dataset-name", default="heart-failure-capstone")
    parser.add_argument("--compute-target", required=True)
    parser.add_argument("--model-name", default="capstone-automl-model")
    parser.add_argument("--timeout-minutes", type=int, default=60)
    args = parser.parse_args()

    ws = get_workspace(args.config)
    experiment = Experiment(workspace=ws, name=args.experiment_name)

    # Load dataset
    dataset = Dataset.get_by_name(ws, name=args.dataset_name)

    # AutoML configuration
    automl_settings = {
        "task": "classification",
        "primary_metric": "accuracy",
        "training_data": dataset,
        "label_column_name": "DEATH_EVENT",
        "n_cross_validations": 5,
        "enable_early_stopping": True,
        "experiment_timeout_minutes": args.timeout_minutes,
        "max_concurrent_iterations": 4,
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
        tags={"project": "capstone", "type": "automl"},
        description="Best model from AutoML",
    )

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/automl_results.json", "w") as f:
        json.dump(
            {
                "automl_run_id": run.id,
                "best_child_run_id": best_run.id,
                "registered_model_name": registered_model.name,
                "registered_model_version": registered_model.version,
                "best_accuracy": best_run.get_metrics().get("accuracy"),
            },
            f,
            indent=2,
        )

    print("AutoML training complete. Results saved to artifacts/automl_results.json")


if __name__ == "__main__":
    main()
