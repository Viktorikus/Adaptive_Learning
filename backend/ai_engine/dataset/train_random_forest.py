import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("adaptive_dataset.csv")

# Encode categorical
le_error = LabelEncoder()
le_action = LabelEncoder()

df["error_type_enc"] = le_error.fit_transform(df["error_type"])
df["next_action_enc"] = le_action.fit_transform(df["next_action"])

X = df[["score", "wrong_count", "error_type_enc"]]
y = df["next_action_enc"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)

# Save model & encoders
joblib.dump(model, "adaptive_rf_model.pkl")
joblib.dump(le_error, "error_encoder.pkl")
joblib.dump(le_action, "action_encoder.pkl")

print("Training selesai")
print("Accuracy:", model.score(X_test, y_test))
