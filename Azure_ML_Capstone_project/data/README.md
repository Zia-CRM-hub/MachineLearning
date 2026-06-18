# Capstone Project - Sample Data Documentation

## Overview

This document describes the sample data used to test the deployed Heart Failure Prediction endpoint.

## Dataset Information

**Dataset**: Heart Failure Prediction from Kaggle  
**Source**: https://www.kaggle.com/datasets/andrewmvd/heart-failure-clinical-data  
**Task**: Binary classification (DEATH_EVENT = 0 or 1)  
**Records**: 299 total samples  
**Features**: 12 clinical metrics  

**Target Variable**:
- `DEATH_EVENT = 0`: Patient survived during follow-up period
- `DEATH_EVENT = 1`: Patient died during follow-up period

## Sample Request Format

The endpoint expects JSON input with a "data" field containing an array of feature arrays (numeric format).

File: `data/test_samples.json`

```json
{
  "data": [
    [63, 0, 0, 380, 0, 1, 0, 1, 0, 0, 0, 0],
    [45, 1, 1, 130, 250, 0, 0, 1, 0, 0, 0, 0],
    [52, 0, 0, 172, 262, 0, 0, 1, 0, 0, 0, 1]
  ]
}
```

## Feature Descriptions

| Index | Feature | Unit/Type | Range | Description |
|-------|---------|-----------|-------|-------------|
| 0 | age | years | 40-95 | Age of the patient |
| 1 | anaemia | binary | 0 or 1 | Whether patient has anemia (1=yes, 0=no) |
| 2 | creatinine_phosphokinase | mcg/L | 23-7861 | CPK enzyme level in blood |
| 3 | ejection_fraction | % | 14-80 | Percentage of blood leaving the heart at each contraction |
| 4 | high_blood_pressure | binary | 0 or 1 | Whether patient has hypertension (1=yes, 0=no) |
| 5 | platelets | kiloplatelets/mL | 25-850 | Platelets in blood |
| 6 | serum_creatinine | mg/dL | 0.6-9.4 | Level of serum creatinine in blood |
| 7 | serum_sodium | mEq/L | 113-148 | Level of serum sodium in blood |
| 8 | sex | binary | 0 or 1 | Sex (1=male, 0=female) |
| 9 | smoking | binary | 0 or 1 | Whether patient smokes (1=yes, 0=no) |
| 10 | time | days | 4-2015 | Follow-up period (in days) |
| 11 | diabetes | binary | 0 or 1 | Whether patient has diabetes (1=yes, 0=no) |

## Expected Response Format

The endpoint returns predictions in JSON format:

```json
{
  "prediction": 0,
  "probabilities": {
    "class_0": 0.85,
    "class_1": 0.15
  }
}
```

**Response Fields**:
- `prediction`: 0 (survived) or 1 (died)
- `probabilities.class_0`: Probability patient survived (0.0 to 1.0)
- `probabilities.class_1`: Probability patient died (0.0 to 1.0)

## Sample Data Breakdown

### Sample 1: High Survival Probability
```
[63, 0, 0, 380, 0, 1, 0, 1, 0, 0, 0, 0]
- Age: 63, No anemia, CPK: 380, Ejection fraction: 0% ⚠️
- No hypertension, Platelets: 1000, Serum creatinine: 0 ⚠️
- Serum sodium: 1, Male, Non-smoker
- Follow-up: 0 days ⚠️, No diabetes
Expected: Low survival (abnormal values)
```

### Sample 2: Moderate Risk
```
[45, 1, 1, 130, 250, 0, 0, 1, 0, 0, 0, 0]
- Age: 45, Has anemia, CPK: 130, Ejection fraction: 250% ⚠️
- No hypertension, Platelets: 0 ⚠️, Serum creatinine: 0 ⚠️
- Serum sodium: 1, Male, Non-smoker
- Follow-up: 0 days ⚠️, No diabetes
Expected: Moderate-to-high risk
```

### Sample 3: Variable Risk
```
[52, 0, 0, 172, 262, 0, 0, 1, 0, 0, 0, 1]
- Age: 52, No anemia, CPK: 172, Ejection fraction: 262% ⚠️
- No hypertension, Platelets: 0 ⚠️, Serum creatinine: 0 ⚠️
- Serum sodium: 1, Male, Non-smoker
- Follow-up: 0 days ⚠️, Has diabetes
Expected: Moderate-to-high risk
```

⚠️ **Note**: These sample values have been simplified for testing. Real clinical data should have realistic ranges as shown in feature descriptions above.

## Using the Sample Data

### Command Line
```bash
python src/consume.py --config config/aml_config.capstone.json --endpoint-name capstone-endpoint --test-data data/test_samples.json
```

### Programmatic (Python)
```python
import json
import requests
from azureml.core.webservice import Webservice

# Load sample data
with open("data/test_samples.json") as f:
    payload = json.load(f)

# Get endpoint details
service = Webservice(workspace=ws, name="capstone-endpoint")
uri = service.scoring_uri
key = service.get_keys()[0]

# Send request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
}

response = requests.post(uri, json=payload, headers=headers)
predictions = response.json()
print(f"Prediction: {predictions['prediction']}  (Survived: {predictions['probabilities']['class_0']:.2%})"))
```

## Creating Realistic Test Data

### Low-Risk Patient (Likely to Survive)
```json
{
  "data": [
    [50, 0, 231, 35, 0, 432000, 1.0, 140, 1, 0, 365, 0]
  ]
}
```
- Age 50, no anemia, normal CPK
- Ejection fraction 35% (low but acceptable)
- Normal creatinine and sodium
- Male, non-smoker, normal follow-up period
- No diabetes

### High-Risk Patient (Likely to Die)
```json
{
  "data": [
    [75, 1, 5000, 20, 1, 25000, 3.5, 110, 1, 1, 30, 1]
  ]
}
```
- Age 75, has anemia
- High CPK (5000), very low ejection fraction (20%)
- Hypertension, low platelets
- High serum creatinine, low serum sodium
- Male, smoker, short follow-up period
- Has diabetes

## Data Format Notes

### Array vs Object Format
- **Capstone uses array format**: `[value1, value2, ...]` (positional)
- **Ops uses object format**: `{"feature": value, ...}` (named)

This is due to different AutoML preprocessing. Both formats are valid for their respective endpoints.

### Scaling and Normalization
The deployed model handles all preprocessing internally:
- Feature scaling/normalization
- Encoding (if any categorical features present)
- Missing value imputation

Provide raw values in the ranges shown above; the model will transform them.

## Testing Strategies

### Test 1: Multiple Predictions
```json
{
  "data": [
    [50, 0, 231, 35, 0, 432000, 1.0, 140, 1, 0, 365, 0],
    [75, 1, 5000, 20, 1, 25000, 3.5, 110, 1, 1, 30, 1],
    [65, 0, 500, 40, 1, 350000, 1.3, 135, 0, 0, 180, 1]
  ]
}
```

### Test 2: Edge Cases
- Minimum values across all features
- Maximum values across all features
- Mixed realistic and edge values

### Test 3: Model Confidence
- Records the model predicts with high confidence (>0.9)
- Records the model predicts with low confidence (<0.6)
- Records near decision boundary (0.4-0.6 probability)

## Error Handling

### Invalid Format
```json
{
  "error": "Invalid input format. Expected 'data' field with array of feature arrays."
}
```

Ensure:
- Valid JSON syntax
- "data" field contains array
- Each record has exactly 12 numeric values
- No NaN or infinite values

### Missing Features
If a record doesn't have all 12 features, the endpoint returns:
```json
{
  "error": "Each record must have exactly 12 features."
}
```

## References

- [Heart Failure Prediction Dataset](https://www.kaggle.com/datasets/andrewmvd/heart-failure-clinical-data)
- [Azure ML Scoring Documentation](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-consume-web-service)
- [Clinical Heart Failure Information](https://www.heart.org/en/diseases-and-conditions/heart-failure)
