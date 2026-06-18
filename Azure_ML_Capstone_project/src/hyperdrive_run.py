import argparse
import json
import os

from azureml.core import Dataset, Experiment
from azureml.core.compute import ComputeTarget, ComputeTargetException
from azureml.core.compute_target import ComputeTargetException
from azureml.train.hyperdrive import (
    GridParameterSampling,
    HyperDriveConfig,
    PrimaryMetricGoal,
    choice,
    uniform,
)

from aml_utils import add_workspace_args, get_workspace


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--experiment-name", default="capstone-hyperdrive")
    parser.add_argument("--dataset-name", default="heart-failure-capstone")
    parser.add_argument("--compute-target", required=True)
    parser.add_argument("--param-sampling", default="grid", choices=["grid", "random"])
    args = parser.parse_args()

    ws = get_workspace(args.config)
    experiment = Experiment(workspace=ws, name=args.experiment_name)

    # Load dataset
    dataset = Dataset.get_by_name(ws, name=args.dataset_name)

    # Hyperparameter space
    param_sampling = GridParameterSampling(
        {
            "--C": choice(0.1, 1.0, 10.0),
            "--max-iter": choice(100, 200, 300),
            "--solver": choice("lbfgs", "saga"),
        }
    )

    # HyperDrive configuration
    hyperdrive_config = HyperDriveConfig(
        run_config=None,  # To be set with training script
        hyperparameter_sampling=param_sampling,
        primary_metric_name="accuracy",
        primary_metric_goal=PrimaryMetricGoal.MAXIMIZE,
        max_total_runs=8,
        max_concurrent_runs=4,
    )

    print(
        "HyperDrive configuration created. Run with: python src/train_hyperdrive.py"
    )
    print("This scaffold requires a training script to execute HyperDrive runs.")


if __name__ == "__main__":
    main()
