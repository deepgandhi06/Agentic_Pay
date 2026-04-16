import json
import os



WALLET_FILE = "wallet_data.json"


def get_wallet_data(address):
    with open(WALLET_FILE, "r") as f:
        data = json.load(f)
    return data.get(address)


def get_private_key(address):
    wallet = get_wallet_data(address)
    return wallet.get("private_key")


def update_daily_wallet_txn_count(address):
    with open(WALLET_FILE, "r") as f:
        data = json.load(f)

    if address in data:
        data[address]["daily_txn_count"] += 1

    with open(WALLET_FILE, "w") as f:
        json.dump(data, f, indent=4)
