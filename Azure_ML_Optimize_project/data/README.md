# Sample Data for Optimize Project

This directory contains sample training and test data for the Azure ML Optimize project.

## Data Format

The project expects CSV files with:
- **Columns**: Feature columns (X1, X2, X3, ...) + target label (y)
- **Rows**: Individual samples
- **Target**: Binary classification (0 or 1)

## Sample Data Files

- `train_test_data.csv` - Combined dataset for splitting
- `train.csv` - Training subset (80% of data)
- `test.csv` - Testing subset (20% of data)

## Feature Descriptions

Typical features might include:
- Numeric features: Age, income, score, duration, etc.
- Categorical features (encoded): Job type, location, category, etc.

## Data Preprocessing

Both HyperDrive and AutoML handle:
- Feature scaling/normalization
- Missing value imputation
- Categorical encoding
- Train/test split management

See main README.md for architecture details.
