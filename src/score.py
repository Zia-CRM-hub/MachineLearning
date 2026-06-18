import json
from pathlib import Path

import joblib
import pandas as pd
from azureml.core.model import Model

MODEL = None


def init():
    global MODEL
    model_path = Model.get_model_path(model_name="bankmarketing-automl-model")
    if not Path(model_path).exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")
    MODEL = joblib.load(model_path)


def run(raw_data):
    try:
        payload = json.loads(raw_data)
        rows = payload.get("data", payload)

        if isinstance(rows, dict):
            rows = [rows]

        frame = pd.DataFrame(rows)
        predictions = MODEL.predict(frame).tolist()

        response = {
            "predictions": predictions,
            "count": len(predictions),
        }
        return json.dumps(response)
    except Exception as ex:
        return json.dumps({"error": str(ex)})
import json
from pathlib import Path

import joblib
import pandas as pd
from azureml.core.model import Model

MODEL = None


def init():
    global MODEL
    model_path = Model.get_model_path(model_name="bankmarketing-automl-model")
    if not Path(model_path).exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")
    MODEL = joblib.load(model_path)


def run(raw_data):
    try:
        payload = json.loads(raw_data)
        rows = payload.get("data", payload)

        if isinstance(rows, dict):
            rows = [rows]

        frame = pd.DataFrame(rows)
        predictions = MODEL.predict(frame).tolist()

        response = {
            "predictions": predictions,
            "count": len(predictions),
        }
        return json.dumps(response)
    except Exception as ex:
        return json.dumps({"error": str(ex)})
