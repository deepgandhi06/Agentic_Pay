import json
import os
from datetime import datetime

PASSBOOK_FILE = "transaction_passbook.json"


def load_passbook():
    if not os.path.exists(PASSBOOK_FILE):
        return []

    with open(PASSBOOK_FILE, "r") as f:
        return json.load(f)


def save_passbook(entries):
    with open(PASSBOOK_FILE, "w") as f:
        json.dump(entries, f, indent=4)


def add_transaction_entry(from_address, to_address, amount, tx_hash, status):

    entries = load_passbook()

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "from_address": from_address,
        "to_address": to_address,
        "amount": amount,
        "tx_hash": tx_hash,
        "status": status
    }

    entries.append(entry)
    save_passbook(entries)
