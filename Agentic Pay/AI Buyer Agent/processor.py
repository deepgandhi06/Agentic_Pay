import sys
import os

from validators import (
    validate_email,
    validate_invoice_id,
    validate_wallet,
    validate_network,
    validate_currency,
    validate_amount
)

from wallet_store import (
    get_wallet_data,
    update_daily_wallet_txn_count
)

from ml_client import send_to_ml

from crypto_client import execute_crypto_transaction


from passbook_store import add_transaction_entry
from wallet_store import get_private_key


HARDCODED_FROM_WALLET = "0x16361fc0c1294b7e24F9A7f68245Da160D72b01D"


def process_invoice_data(invoice):

    data = invoice.model_dump()

    processed_invoices = set()

    invoice_id = data.get("invoice_id")

    # 🔒 Prevent duplicate invoice processing
    if invoice_id in processed_invoices:
        print(f"⚠️ Duplicate invoice detected: {invoice_id}")
        return {
            "status": "duplicate_invoice",
            "reason": "invoice_already_processed"
        }

    # Hardcode sender wallet
    data["from_wallet"] = HARDCODED_FROM_WALLET

    email_valid = validate_email(data.get("sender_email"))
    invoice_valid = validate_invoice_id(data.get("invoice_id"))
    wallet_valid = validate_wallet(data.get("to_wallet"))
    network_valid = validate_network(data.get("network"))
    currency_valid = validate_currency(data.get("currency"))
    amount_valid = validate_amount(data.get("amount"))

    if not (email_valid and invoice_valid and wallet_valid and
            network_valid and currency_valid and amount_valid):
        
        print("Email Valid     :", email_valid)
        print("Invoice Valid   :", invoice_valid)
        print("Wallet Valid    :", wallet_valid)
        print("Network Valid   :", network_valid)
        print("Currency Valid  :", currency_valid)
        print("Amount Valid    :", amount_valid)


        return {
            "status": "rejected_before_ml",
            "reason": "basic_validation_failed"
        }

    if data.get("network").lower() != "ethereum":
        return {
            "status": "rejected",
            "reason": "unsupported_network"
        }

    to_wallet = data.get("to_wallet")
    from_wallet = data.get("from_wallet")

    wallet_data = get_wallet_data(to_wallet)

    features = {
        "amount": data.get("amount", 0),
        "wallet_age_days": wallet_data["wallet_age_days"],
        "daily_txn_count": wallet_data["daily_txn_count"],
        "kyc_status": wallet_data["kyc_status"],
        "email_valid": email_valid,
        "unusual_time": wallet_data["unusual_time"],
        "device_new": wallet_data["device_new"],
        "geo_mismatch": wallet_data["geo_mismatch"],
        "network_flag": 1 if data.get("network") == "ethereum" else 0,
        "label": 0
    }

    ml_response = send_to_ml(features)

    decision = ml_response.get("decision")
    risk_score = ml_response.get("risk_score")

    if decision == "PROCEED":

        private_key = get_private_key(from_wallet)

        result = execute_crypto_transaction(data, private_key)

        update_daily_wallet_txn_count(from_wallet)

        add_transaction_entry(
            from_address=from_wallet,
            to_address=to_wallet,
            amount=data.get("amount"),
            tx_hash=result.get("txId"),
            status=result.get("status")
        )

        return {
            "status": "approved_and_executed",
            "risk_score": risk_score,
            "tx_hash": result.get("txId")
        }

    return {
        "status": "rejected_by_ml",
        "risk_score": risk_score
    }
