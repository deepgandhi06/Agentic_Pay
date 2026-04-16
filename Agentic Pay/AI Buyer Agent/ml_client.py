import requests

ML_SERVICE_URL = "http://127.0.0.1:8003/check-risk"

def send_to_ml(features: dict) -> dict:
    try:
        response = requests.post(
            ML_SERVICE_URL,
            json=features,
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {
            "error": "ML service call failed",
            "details": str(e)
        }
