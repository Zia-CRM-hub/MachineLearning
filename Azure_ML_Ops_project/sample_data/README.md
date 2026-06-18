# Ops Project - Sample Data Documentation

## Overview

This document describes the sample data used to test the deployed Bank Marketing endpoint.

## Dataset Information

**Dataset**: Bank Marketing  
**Source**: https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv  
**Task**: Binary classification (y = "yes" or "no" - client subscribes to term deposit)  
**Records**: 4521 training samples  
**Features**: 16 features (age, job, marital status, education, etc.)  

## Sample Request Format

The endpoint expects JSON input with a "data" field containing an array of feature dictionaries.

### Raw Format (Categorical)
File: `sample_data/sample_request.json`

```json
{
  "data": [
    {
      "age": 33,
      "job": "technician",
      "marital": "married",
      "education": "secondary",
      "default": "no",
      "balance": 1200,
      "housing": "yes",
      "loan": "no",
      "contact": "cellular",
      "day": 5,
      "month": "may",
      "duration": 120,
      "campaign": 1,
      "pdays": -1,
      "previous": 0,
      "poutcome": "unknown"
    }
  ]
}
```

### Feature Descriptions

| Feature | Type | Description | Example Values |
|---------|------|-------------|-----------------|
| age | int | Age of client | 18-95 |
| job | string | Type of job | technician, services, management, retired, etc. |
| marital | string | Marital status | married, single, divorced |
| education | string | Education level | primary, secondary, tertiary, unknown |
| default | string | Has credit in default? | yes, no |
| balance | int | Account balance in euros | -8019 to 102127 |
| housing | string | Has housing loan? | yes, no |
| loan | string | Has personal loan? | yes, no |
| contact | string | Contact communication type | cellular, telephone |
| day | int | Day of month last contacted | 1-31 |
| month | string | Month of last contact | january, february, ..., december |
| duration | int | Duration of last contact in seconds | 0-4918 |
| campaign | int | Number of contacts during campaign | 1-56 |
| pdays | int | Days since previous campaign contact | -1 (never contacted) or 0-999 |
| previous | int | Number of contacts before campaign | 0-7 |
| poutcome | string | Outcome of previous campaign | success, failure, unknown |

## Expected Response Format

The endpoint returns predictions in JSON format:

```json
{
  "prediction": "yes",
  "probability": 0.75
}
```

**Response Fields**:
- `prediction`: "yes" (subscribed) or "no" (did not subscribe)
- `probability`: Confidence score (0.0 to 1.0)

## Using the Sample Data

### Command Line
```bash
python src/consume_endpoint.py --service-name bankmarketing-service --input-json sample_data/sample_request.json
```

### Programmatic (Python)
```python
import json
import requests
from azureml.core.webservice import Webservice

# Load sample data
with open("sample_data/sample_request.json") as f:
    payload = json.load(f)

# Get endpoint details
service = Webservice(workspace=ws, name="bankmarketing-service")
uri = service.scoring_uri
key = service.get_keys()[0]

# Send request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
}

response = requests.post(uri, json=payload, headers=headers)
print(response.json())
```

## Sample Data Variations

### High Probability of "Yes" (Likely to Subscribe)
```json
{
  "data": [
    {
      "age": 25,
      "job": "technician",
      "marital": "single",
      "education": "tertiary",
      "default": "no",
      "balance": 5000,
      "housing": "no",
      "loan": "no",
      "contact": "cellular",
      "day": 15,
      "month": "may",
      "duration": 500,
      "campaign": 1,
      "pdays": -1,
      "previous": 0,
      "poutcome": "unknown"
    }
  ]
}
```

### Low Probability of "Yes" (Unlikely to Subscribe)
```json
{
  "data": [
    {
      "age": 75,
      "job": "retired",
      "marital": "married",
      "education": "primary",
      "default": "yes",
      "balance": -5000,
      "housing": "yes",
      "loan": "yes",
      "contact": "telephone",
      "day": 1,
      "month": "january",
      "duration": 10,
      "campaign": 10,
      "pdays": 30,
      "previous": 5,
      "poutcome": "failure"
    }
  ]
}
```

## Data Preprocessing Notes

The AutoML model automatically handles:
- **Categorical Encoding**: Job, marital, education, etc. are one-hot encoded
- **Scaling**: Numeric features are normalized
- **Missing Values**: Handled during training
- **Feature Engineering**: AutoML may create derived features

The raw JSON data above is what you provide to the endpoint; the model expects this format and handles transformation internally.

## Testing

### Test Multiple Records
The endpoint accepts multiple records in a single request:

```json
{
  "data": [
    { "age": 25, "job": "technician", ... },
    { "age": 35, "job": "manager", ... },
    { "age": 45, "job": "retired", ... }
  ]
}
```

Response will include predictions for all records.

### Error Handling

If the request format is invalid, you may receive:
```json
{
  "error": "Invalid input format. Expected 'data' field with array of records."
}
```

Ensure:
- Request is valid JSON
- All required features are present
- Data types match (string vs int)
- No extra/unknown features

## References

- [Bank Marketing Dataset Paper](https://archive.ics.uci.edu/dataset/222/bank+marketing)
- [Azure ML Scoring Endpoint Documentation](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-consume-web-service)
