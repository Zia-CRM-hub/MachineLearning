"""
AutoML Configuration and Execution

Configures AutoML to automatically find the best classification model.
"""

import argparse
from azureml.core import Workspace, Experiment, Dataset
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.train.automl import AutoMLConfig
from src.aml_utils import get_workspace, load_config, add_workspace_args
import json


def setup_automl(training_dataset, experiment_name="optimize-automl"):
    """
    Configure AutoML for classification task.
    
    Args:
        training_dataset: Registered training dataset
        experiment_name: Experiment name
        
    Returns:
        AutoML configuration
    """
    
    automl_config = AutoMLConfig(
        task="classification",
        primary_metric="accuracy",
        experiment_timeout_minutes=60,
        training_data=training_dataset,
        label_column_name="y",
        n_cross_validations=5,
        max_concurrent_iterations=4,
        enable_early_stopping=True,
        verbosity=logging.INFO
    )
    
    return automl_config


def submit_automl_run(ws, automl_config, experiment_name="optimize-automl"):
    """
    Submit AutoML run to Azure ML.
    
    Args:
        ws: Azure ML Workspace
        automl_config: AutoML configuration
        experiment_name: Experiment name
        
    Returns:
        AutoML run object
    """
    experiment = Experiment(ws, experiment_name)
    automl_run = experiment.submit(automl_config, show_output=True)
    
    return automl_run


def main():
    """Main entry point for AutoML configuration and submission."""
    
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--dataset-name", type=str, default="optimize-dataset")
    parser.add_argument("--experiment-name", type=str, default="optimize-automl")
    parser.add_argument("--model-name", type=str, default="optimize-automl-model")
    
    args = parser.parse_args()
    
    # Get workspace
    ws = get_workspace(args.config)
    print(f"Workspace: {ws.name}")
    
    # Get dataset
    dataset = Dataset.get_by_name(ws, args.dataset_name)
    print(f"Dataset '{args.dataset_name}' loaded")
    
    # Setup AutoML
    automl_config = setup_automl(dataset, args.experiment_name)
    
    # Submit run
    automl_run = submit_automl_run(ws, automl_config, args.experiment_name)
    print(f"AutoML run submitted: {automl_run.id}")
    
    # Get best model
    best_run, fitted_model = automl_run.get_output()
    best_accuracy = best_run.get_metrics()["accuracy"]
    
    # Register best model
    best_run.register_model(
        model_name=args.model_name,
        model_path="outputs/model.pkl"
    )
    
    # Save results
    results = {
        "automl_run_id": automl_run.id,
        "best_run_id": best_run.id,
        "best_accuracy": best_accuracy,
        "best_model_name": args.model_name,
        "algorithm": best_run.properties.get("model_name", "Unknown")
    }
    
    with open("artifacts/automl_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Best accuracy: {best_accuracy:.4f}")
    print(f"Best algorithm: {results['algorithm']}")
    print("Results saved to artifacts/automl_results.json")


if __name__ == "__main__":
    main()
