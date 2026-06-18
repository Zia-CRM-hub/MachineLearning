import argparse
import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bankmarketing", type=str, required=True)
    parser.add_argument("--model-output", type=str, required=True)
    args = parser.parse_args()

    input_path = Path(args.bankmarketing)
    if input_path.is_dir():
        csv_files = list(input_path.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in input folder: {input_path}")
        input_path = csv_files[0]

    df = pd.read_csv(input_path)
    if "y" not in df.columns:
        raise ValueError("Expected target column 'y' in bank marketing dataset")

    y = (df["y"].astype(str).str.lower() == "yes").astype(int)
    X = df.drop(columns=["y"])

    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]),
                numeric_cols,
            ),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_cols,
            ),
        ]
    )

    clf = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", LogisticRegression(max_iter=1000)),
        ]
    )

    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf.fit(X_train, y_train)
    probas = clf.predict_proba(X_valid)[:, 1]
    auc = roc_auc_score(y_valid, probas)
    print(f"Validation ROC AUC: {auc:.4f}")

    os.makedirs(args.model_output, exist_ok=True)
    model_path = Path(args.model_output) / "pipeline_model.pkl"
    joblib.dump(clf, model_path)
    print(f"Saved model to: {model_path}")


if __name__ == "__main__":
    main()
