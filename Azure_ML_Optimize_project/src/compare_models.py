"""
Compare HyperDrive and AutoML Models

Loads results from both HyperDrive and AutoML experiments,
compares their performance, and selects the best model.
"""

import json
from pathlib import Path


def compare_models():
    """
    Compare HyperDrive and AutoML results.
    
    Returns:
        Dictionary with comparison results
    """
    
    # Load HyperDrive results
    with open("artifacts/hyperdrive_results.json") as f:
        hyperdrive_results = json.load(f)
    
    # Load AutoML results
    with open("artifacts/automl_results.json") as f:
        automl_results = json.load(f)
    
    hyperdrive_accuracy = hyperdrive_results["best_accuracy"]
    automl_accuracy = automl_results["best_accuracy"]
    
    # Determine winner
    if hyperdrive_accuracy > automl_accuracy:
        winner = "hyperdrive"
        winning_accuracy = hyperdrive_accuracy
        winning_model_name = hyperdrive_results.get("best_run_id")
    else:
        winner = "automl"
        winning_accuracy = automl_accuracy
        winning_model_name = automl_results.get("best_model_name")
    
    # Create comparison results
    comparison = {
        "hyperdrive_accuracy": hyperdrive_accuracy,
        "hyperdrive_hyperparameters": hyperdrive_results.get("best_hyperparameters"),
        "automl_accuracy": automl_accuracy,
        "automl_algorithm": automl_results.get("algorithm"),
        "winner": winner,
        "winning_accuracy": winning_accuracy,
        "winning_model_name": winning_model_name,
        "accuracy_difference": abs(hyperdrive_accuracy - automl_accuracy)
    }
    
    return comparison


def main():
    """Main entry point for model comparison."""
    
    print("Comparing HyperDrive and AutoML models...")
    
    comparison = compare_models()
    
    # Display results
    print("\n" + "="*60)
    print("MODEL COMPARISON RESULTS")
    print("="*60)
    print(f"\nHyperDrive Accuracy: {comparison['hyperdrive_accuracy']:.4f}")
    print(f"  Parameters: {comparison['hyperdrive_hyperparameters']}")
    
    print(f"\nAutoML Accuracy: {comparison['automl_accuracy']:.4f}")
    print(f"  Algorithm: {comparison['automl_algorithm']}")
    
    print(f"\nWinner: {comparison['winner'].upper()}")
    print(f"Winning Accuracy: {comparison['winning_accuracy']:.4f}")
    print(f"Accuracy Difference: {comparison['accuracy_difference']:.4f}")
    
    # Save comparison
    with open("artifacts/comparison_results.json", "w") as f:
        json.dump(comparison, f, indent=2)
    
    print("\nComparison saved to artifacts/comparison_results.json")


if __name__ == "__main__":
    main()
