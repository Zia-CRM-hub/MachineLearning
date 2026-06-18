import json
from pathlib import Path


def main():
    # Load results from both runs
    with open("artifacts/automl_results.json") as f:
        automl = json.load(f)

    with open("artifacts/hyperdrive_results.json") as f:
        hyperdrive = json.load(f)

    # Compare metrics
    automl_accuracy = automl.get("best_accuracy", 0)
    hyperdrive_accuracy = hyperdrive.get("best_accuracy", 0)

    winner = "AutoML" if automl_accuracy >= hyperdrive_accuracy else "HyperDrive"

    comparison = {
        "automl_accuracy": automl_accuracy,
        "hyperdrive_accuracy": hyperdrive_accuracy,
        "winner": winner,
        "winning_accuracy": max(automl_accuracy, hyperdrive_accuracy),
        "winning_model_name": automl.get("registered_model_name")
        if winner == "AutoML"
        else hyperdrive.get("registered_model_name"),
    }

    with open("artifacts/comparison_results.json", "w") as f:
        json.dump(comparison, f, indent=2)

    print(f"Model Comparison Results:")
    print(f"  AutoML Accuracy: {automl_accuracy:.4f}")
    print(f"  HyperDrive Accuracy: {hyperdrive_accuracy:.4f}")
    print(f"  Winner: {winner}")
    print(f"Results saved to artifacts/comparison_results.json")


if __name__ == "__main__":
    main()
