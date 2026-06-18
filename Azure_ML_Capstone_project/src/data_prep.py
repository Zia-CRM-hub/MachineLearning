import argparse
import json
import os
from pathlib import Path

import pandas as pd
from azureml.core import Dataset, Workspace

from aml_utils import add_workspace_args, get_workspace


def main():
    parser = argparse.ArgumentParser()
    add_workspace_args(parser)
    parser.add_argument("--input-data", required=True, help="Path to CSV data file")
    parser.add_argument("--dataset-name", default="heart-failure-capstone")
    parser.add_argument("--test-size", type=float, default=0.2)
    args = parser.parse_args()

    ws = get_workspace(args.config)

    # Load and preprocess data
    df = pd.read_csv(args.input_data)

    # Basic preprocessing
    if df.isnull().sum().sum() > 0:
        df.dropna(inplace=True)

    # Register dataset
    dataset = Dataset.Tabular.from_delimited_files(path=args.input_data)
    dataset = dataset.register(
        workspace=ws,
        name=args.dataset_name,
        create_new_version=True,
        description="Heart failure prediction dataset",
    )

    # Save prep metadata
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/data_prep.json", "w") as f:
        json.dump(
            {
                "dataset_name": dataset.name,
                "dataset_id": dataset.id,
                "num_rows": len(df),
                "num_features": len(df.columns),
                "test_size": args.test_size,
            },
            f,
            indent=2,
        )

    print(f"Dataset {args.dataset_name} registered successfully.")
    print(f"Total records: {len(df)}, Features: {len(df.columns)}")


if __name__ == "__main__":
    main()
