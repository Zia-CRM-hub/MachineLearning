import argparse
import json

from joblib import dump
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from azureml.core import Run
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--C", type=float, default=1.0)
    parser.add_argument("--max-iter", type=int, default=100)
    parser.add_argument("--solver", default="lbfgs")
    args = parser.parse_args()

    run = Run.get_context()

    # Load data
    try:
        X = pd.read_csv("data/X_train.csv")
        y = pd.read_csv("data/y_train.csv").squeeze()
    except FileNotFoundError:
        print("Training data not found. Using dummy data for demo.")
        X = pd.DataFrame([[1, 2, 3]] * 100, columns=["f1", "f2", "f3"])
        y = pd.Series([0, 1] * 50)

    # Split and train
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)

    model = LogisticRegression(
        C=args.C, max_iter=args.max_iter, solver=args.solver, random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_val, y_val)
    run.log("accuracy", accuracy)

    # Save
    import os

    os.makedirs("outputs", exist_ok=True)
    dump(model, "outputs/model.pkl")

    print(f"Training complete. Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()
