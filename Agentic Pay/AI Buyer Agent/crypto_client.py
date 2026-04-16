import requests
import time
import logging

import requests
import logging

BASE_URL = "http://localhost:9090/api"

logging.basicConfig(level=logging.INFO)


def send_transfer(to_address: str, amount: float, private_key: str):

    payload = {
        "receiver": to_address,
        "amount": amount,
        "privateKey": private_key
    }

    try:
        response = requests.post(f"{BASE_URL}/transfer", json=payload)
        response.raise_for_status()

        data = response.json()

        tx_hash = data.get("txHash")
        status = data.get("status")

        logging.info(f"✅ Transfer initiated. Hash: {tx_hash}, Status: {status}")

        return tx_hash, status

    except requests.RequestException as e:
        logging.error(f"❌ Transfer failed: {e}")
        return None, None


def execute_crypto_transaction(invoice_data: dict, private_key: str):

    tx_hash, status = send_transfer(
        to_address=invoice_data.get("to_wallet"),
        amount=invoice_data.get("amount"),
        private_key=private_key
    )

    if not tx_hash:
        return {
            "status": "transfer_failed"
        }

    return {
        "status": status.lower(),
        "txId": tx_hash
    }
