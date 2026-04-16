import json
import os

FILE_PATH = "account_data.json"

def read_store():
    if not os.path.exists(FILE_PATH):
        return {}

    with open(FILE_PATH, "r") as f:
        return json.load(f)


def write_store(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def get_account_data(account_number: str) -> dict:
    store = read_store()

    return store.get(account_number, {
        "account_age_days": 0,
        "daily_txn_count": 0,
        "kyc_status": 0,
        "device_new": 1,
        "geo_mismatch": 0,
        "unusual_time": 0
    })


def update_daily_txn_count(account_number: str):
    store = read_store()

    if account_number not in store:
        store[account_number] = get_account_data(account_number)

    store[account_number]["daily_txn_count"] += 1

    write_store(store)
