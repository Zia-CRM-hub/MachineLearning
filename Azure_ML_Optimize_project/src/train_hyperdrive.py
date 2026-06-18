"""
Training script executed by HyperDrive.

This script is called for each hyperparameter combination explored by HyperDrive.
It trains a logistic regression model and logs the accuracy metric.
"""

import argparse
import joblib
import json
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from azureml.core import Run
import pandas as pd
import numpy as np


def train_model(C, max_iter, solver, training_data, test_data):
    """
    Train logistic regression model with specified hyperparameters.
    
    Args:
        C: Inverse regularization strength (float)
        max_iter: Maximum iterations (int)
        solver: Optimization algorithm (str)
        training_data: Training DataFrame
        test_data: Test DataFrame
        
    Returns:
        Trained model, accuracy score
    """
    # Separate features and labels
    X_train = training_data.drop('y', axis=1).values
    y_train = training_data['y'].values
    X_test = test_data.drop('y', axis=1).values
    y_test = test_data['y'].values
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train logistic regression
    model = LogisticRegression(
        C=C,
        max_iter=max_iter,
        solver=solver,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    
    # Calculate accuracy
    predictions = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, predictions)
    
    return model, accuracy


def main():
    """
    Main entry point for HyperDrive training script.
    
    Receives hyperparameters from HyperDrive via command-line arguments,
    trains model, and logs metrics for the run.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--C", type=float, default=1.0, help="Regularization strength")
    parser.add_argument("--max-iter", type=int, default=100, help="Max iterations")
    parser.add_argument("--solver", type=str, default="lbfgs", help="Optimization solver")
    parser.add_argument("--train-data", type=str, default="data/train.csv", help="Training data path")
    parser.add_argument("--test-data", type=str, default="data/test.csv", help="Test data path")
    
    args = parser.parse_args()
    
    # Load training and test data
    train_df = pd.read_csv(args.train_data)
    test_df = pd.read_csv(args.test_data)
    
    # Train model
    model, accuracy = train_model(
        C=args.C,
        max_iter=args.max_iter,
        solver=args.solver,
        training_data=train_df,
        test_data=test_df
    )
    
    # Get Run context
    run = Run.get_context()
    
    # Log metrics
    run.log("accuracy", accuracy)
    run.log("C", args.C)
    run.log("max_iter", args.max_iter)
    run.log("solver", args.solver)
    
    # Save model to outputs
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    model_path = output_dir / "model.pkl"
    joblib.dump(model, model_path)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    main()
