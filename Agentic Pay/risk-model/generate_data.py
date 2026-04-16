import pandas as pd
import random

ROWS = 5000
OUTPUT_FILE = "transactions.csv"

data = []

for _ in range(ROWS):
    # 💰 Stablecoin amount
    amount = random.choice([
        random.randint(100, 2000),
        random.randint(2000, 10000),
        random.randint(10000, 100000)
    ])

    wallet_age_days = random.randint(1, 1500)
    daily_txn_count = random.randint(1, 12)
    kyc_status = random.choice([0, 1])
    unusual_time = random.choice([0, 1])
    email_valid = random.choice([0, 1])
    device_new = random.choice([0, 1])
    geo_mismatch = random.choice([0, 1])

    network_flag = 1

    # ---- Stronger Crypto Risk Logic ----
    risk_score = 0

    if amount > 40000:
        risk_score += 2
    if wallet_age_days < 60:
        risk_score += 2
    if daily_txn_count > 8:
        risk_score += 2
    if kyc_status == 0:
        risk_score += 3
    if device_new == 1:
        risk_score += 1
    if geo_mismatch == 1:
        risk_score += 2
    if unusual_time == 1:
        risk_score += 1
    if email_valid == 0:
        risk_score += 2

    # ---- Cleaner Labeling ----
    if risk_score >= 6:
        label = 1
    elif risk_score <= 2:
        label = 0
    else:
        label = 1 if random.random() > 0.7 else 0

    data.append([
        amount,
        wallet_age_days,
        daily_txn_count,
        kyc_status,
        unusual_time,
        email_valid,
        device_new,
        geo_mismatch,
        network_flag,
        label
    ])

columns = [
    "amount",
    "wallet_age_days",
    "daily_txn_count",
    "kyc_status",
    "unusual_time",
    "email_valid",
    "device_new",
    "geo_mismatch",
    "network_flag",
    "label"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Generated {ROWS} realistic crypto transactions → {OUTPUT_FILE}")
