import os
import joblib
import numpy as np

# Path absolut ke folder dataset
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

MODEL_PATH = os.path.join(DATASET_DIR, "adaptive_rf_model.pkl")
ERROR_ENCODER_PATH = os.path.join(DATASET_DIR, "error_encoder.pkl")
ACTION_ENCODER_PATH = os.path.join(DATASET_DIR, "action_encoder.pkl")

# Load model & encoder (sekali saja)
_rf_model = None
_error_encoder = None
_action_encoder = None


def load_adaptive_model():
    """
    Load Random Forest model dan encoder (singleton pattern)
    """
    global _rf_model, _error_encoder, _action_encoder

    if _rf_model is None:
        _rf_model = joblib.load(MODEL_PATH)
        _error_encoder = joblib.load(ERROR_ENCODER_PATH)
        _action_encoder = joblib.load(ACTION_ENCODER_PATH)

    return _rf_model, _error_encoder, _action_encoder


def predict_next_action(score, wrong_count, error_type):
    """
    Prediksi next_action berdasarkan hasil evaluasi siswa

    Parameters:
    - score: float / int
    - wrong_count: int
    - error_type: str ("no_error", "procedural_error", "conceptual_error")
    """

    model, error_encoder, action_encoder = load_adaptive_model()

    try:
        error_encoded = error_encoder.transform([error_type])[0]
    except ValueError:
        # fallback jika error_type tidak dikenali
        error_encoded = error_encoder.transform(["procedural_error"])[0]

    X_input = np.array([[score, wrong_count, error_encoded]])

    pred_enc = model.predict(X_input)[0]
    pred_action = action_encoder.inverse_transform([pred_enc])[0]

    return {
        "next_action": pred_action,
        "input": {
            "score": score,
            "wrong_count": wrong_count,
            "error_type": error_type
        }
    }
