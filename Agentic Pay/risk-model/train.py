# train_model.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os

MODEL_PATH = "model.pkl"
DATA_PATH = "transactions.csv"

def load_model():
    print("🔄 Training ML Risk Model...")

    data = pd.read_csv(DATA_PATH)

    X = data.drop("label", axis=1)
    y = data["label"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("✅ Model trained and saved as model.pkl")

if __name__ == "__main__":
    train_and_save_model()
