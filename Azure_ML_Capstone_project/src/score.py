import json
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice


def init():
    """Initialize model for inference."""
    import joblib
    import os

    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.pkl")
    global model
    model = joblib.load(model_path)


def run(data):
    """Run prediction on input data."""
    import json
    import numpy as np

    try:
        data = json.loads(data)
        features = np.array(data["data"]).reshape(1, -1)
        prediction = model.predict(features)
        probabilities = model.predict_proba(features)

        return {
            "prediction": int(prediction[0]),
            "probabilities": {
                "class_0": float(probabilities[0][0]),
                "class_1": float(probabilities[0][1]),
            },
        }
    except Exception as e:
        return {"error": str(e)}
