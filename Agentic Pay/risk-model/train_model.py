# train_model.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle

MODEL_PATH = "model.pkl"
DATA_PATH = "transactions.csv"


def train_and_save_model():
    print("🔄 Training ML Risk Model with scaling + calibration...")

    # Load data
    data = pd.read_csv(DATA_PATH)

    X = data.drop("label", axis=1)
    y = data["label"]

    # Pipeline: Scaling + Logistic Regression
    base_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("logreg", LogisticRegression(
            max_iter=2000,
            C=0.1,
            class_weight="balanced",
            solver="liblinear"
        ))
    ])

    # Calibrated model (Platt scaling)
    model = CalibratedClassifierCV(
        base_pipeline,
        method="sigmoid",
        cv=3
    )

    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("✅ Calibrated + Scaled model trained and saved as model.pkl")


if __name__ == "__main__":
    train_and_save_model()
