"""
HyperDrive Configuration and Execution

Configures HyperDrive to perform hyperparameter tuning on a Logistic Regression model.
"""

import argparse
from azureml.core import Workspace, Experiment, Dataset, ScriptRunConfig
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.train.hyperdrive import (
    GridParameterSampling,
    HyperDriveConfig,
    PrimaryMetricGoal,
    BanditPolicy
)
from azureml.train.hyperdrive.parameter_expressions import choice, uniform
from src.aml_utils import get_workspace, load_config, add_workspace_args
import json


def setup_hyperdrive(ws, compute_target, training_dataset, test_dataset):
    """
    Configure and return HyperDrive run.
    
    Args:
        ws: Azure ML Workspace
        compute_target: Compute cluster name
        training_dataset: Registered training dataset
        test_dataset: Registered test dataset
        
    Returns:
        HyperDrive run object
    """
    
    # Define parameter search space
    param_sampling = GridParameterSampling({
        "--C": choice([0.1, 1.0, 10.0]),
        "--max-iter": choice([100, 200, 300]),
        "--solver": choice(["lbfgs", "saga"])
    })
    
    # Define early stopping policy
    early_termination_policy = BanditPolicy(
        slack_factor=0.1,
        evaluation_interval=1,
        delay_evaluation=5
    )
    
    # Configure training script run
    script_config = ScriptRunConfig(
        source_directory=".",
        script="src/train_hyperdrive.py",
        compute_target=compute_target,
        arguments=[
            "--train-data", training_dataset.as_mount() + "/train.csv",
            "--test-data", test_dataset.as_mount() + "/test.csv"
        ]
    )
    
    # Create HyperDrive configuration
    hyperdrive_config = HyperDriveConfig(
        run_config=script_config,
        hyperparameter_sampling=param_sampling,
        primary_metric_name="accuracy",
        primary_metric_goal=PrimaryMetricGoal.MAXIMIZE,
        max_total_runs=18,
        max_concurrent_runs=4,
        policy=early_termination_policy
    )
    
    return hyperdrive_config


def submit_hyperdrive_run(ws, hyperdrive_config, experiment_name="optimize-hyperdrive"):
    """
    Submit HyperDrive run to Azure ML.
    
    Args:
        ws: Azure ML Workspace
        hyperdrive_config: HyperDrive configuration
        experiment_name: Experiment name
        
    Returns:
        HyperDrive run object
    """
    experiment = Experiment(ws, experiment_name)
    hyperdrive_run = experiment.submit(hyperdrive_config)
    
    return hyperdrive_run


def main():
    """Main entry point for HyperDrive configuration and submission."""
    
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--dataset-name", type=str, default="optimize-dataset")
    parser.add_argument("--experiment-name", type=str, default="optimize-hyperdrive")
    
    args = parser.parse_args()
    
    # Get workspace
    ws = get_workspace(args.config)
    print(f"Workspace: {ws.name}")
    
    # Get or create compute target
    try:
        compute_target = ComputeTarget(ws, args.compute_target)
        print(f"Compute target '{args.compute_target}' found")
    except ComputeTargetException:
        print(f"Creating compute target '{args.compute_target}'...")
        compute_config = AmlCompute.provisioning_configuration(
            vm_size="Standard_D2s_v3",
            min_nodes=0,
            max_nodes=4
        )
        compute_target = ComputeTarget.create(ws, args.compute_target, compute_config)
        compute_target.wait_for_completion(show_output=True)
    
    # Get dataset
    dataset = Dataset.get_by_name(ws, args.dataset_name)
    print(f"Dataset '{args.dataset_name}' loaded")
    
    # Split dataset into train/test (note: in practice, this would be pre-split)
    train_dataset = dataset
    test_dataset = dataset  # Placeholder - actual implementation would split properly
    
    # Setup HyperDrive
    hyperdrive_config = setup_hyperdrive(ws, compute_target, train_dataset, test_dataset)
    
    # Submit run
    hyperdrive_run = submit_hyperdrive_run(ws, hyperdrive_config, args.experiment_name)
    print(f"HyperDrive run submitted: {hyperdrive_run.id}")
    
    # Get best run
    best_run = hyperdrive_run.get_best_run_by_primary_metric()
    best_accuracy = best_run.get_metrics()["accuracy"]
    best_params = best_run.get_details()["runDefinition"]["arguments"]
    
    # Save results
    results = {
        "hyperdrive_run_id": hyperdrive_run.id,
        "best_run_id": best_run.id,
        "best_accuracy": best_accuracy,
        "best_hyperparameters": {
            "C": best_params.get("C"),
            "max_iter": best_params.get("max_iter"),
            "solver": best_params.get("solver")
        }
    }
    
    with open("artifacts/hyperdrive_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Best accuracy: {best_accuracy:.4f}")
    print("Results saved to artifacts/hyperdrive_results.json")


if __name__ == "__main__":
    main()
