# api.py
from fastapi import APIRouter
import pandas as pd

router = APIRouter()

# model will be injected from main
model = None

def set_model(loaded_model):
    global model
    model = loaded_model


@router.get("/")
def health_check():
    return {"status": "Crypto ML Risk Service Running"}


@router.post("/check-risk")
def check_risk(transaction: dict):
    """
    Expected fields:
    amount,
    wallet_age_days,
    daily_txn_count,
    kyc_status,
    unusual_time,
    email_valid,
    device_new,
    geo_mismatch,
    network_flag
    """

    # ✅ Create DataFrame with SAME column order used during training
    features = pd.DataFrame([{
        "amount": transaction["amount"],
        "wallet_age_days": transaction["wallet_age_days"],
        "daily_txn_count": transaction["daily_txn_count"],
        "kyc_status": transaction["kyc_status"],
        "unusual_time": transaction["unusual_time"],
        "email_valid": transaction["email_valid"],
        "device_new": transaction["device_new"],
        "geo_mismatch": transaction["geo_mismatch"],
        "network_flag": transaction["network_flag"]
    }])

    prediction = model.predict(features)[0]
    risk_score = model.predict_proba(features)[0][1]

    return {
        "decision": "REJECT" if prediction == 1 else "PROCEED",
        "risk_score": round(float(risk_score), 2)
    }
