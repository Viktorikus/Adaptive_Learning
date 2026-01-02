from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Encoding error type
ERROR_MAP = {
    "no_error": 0,
    "procedural_error": 1,
    "conceptual_error": 2
}

STRATEGY_MAP = {
    0: "advanced_practice",
    1: "guided_practice",
    2: "remedial_concept"
}

def train_dummy_model():
    """
    Dataset simulasi (sementara)
    """

    X = np.array([
        [0, 0, 100],   # no_error
        [1, 1, 66],    # procedural
        [2, 3, 33],    # conceptual
        [1, 2, 50],
        [2, 3, 20]
    ])

    y = np.array([
        0,  # advanced
        1,  # guided
        2,  # remedial
        1,
        2
    ])

    model = RandomForestClassifier(
        n_estimators=50,
        random_state=42
    )

    model.fit(X, y)
    return model

_model = train_dummy_model()

def predict_learning_strategy(error_type, wrong_count, score):
    error_encoded = ERROR_MAP.get(error_type, 1)

    X_input = np.array([[error_encoded, wrong_count, score]])

    pred = _model.predict(X_input)[0]

    return STRATEGY_MAP[pred]