# model_loader.py
import pickle
import os
from train_model import train_and_save_model

MODEL_PATH = "model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()

    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)
