import re
from datetime import datetime

# 🚫 Block suspicious email formats
BLOCKED_EMAIL_PATTERNS = [
    r".*\+.*@gmail\.com",
    r"^[0-9]{6,}@gmail\.com",
    r".*temp.*@gmail\.com"
]

# -------------------------------
# 📧 Email Validation
# -------------------------------
def validate_email(email: str) -> int:
    if not email:
        return 0

    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(regex, email):
        return 0

    for pattern in BLOCKED_EMAIL_PATTERNS:
        if re.match(pattern, email):
            return 0

    return 1


# -------------------------------
# 🧾 Invoice ID Validation
# Example: INV-44321
# -------------------------------
def validate_invoice_id(invoice_id: str) -> int:
    if not invoice_id:
        return 0

    return 1 if re.match(r"^INV-\d{4,10}$", invoice_id) else 0


# -------------------------------
# 💰 Stablecoin Validation
# -------------------------------
SUPPORTED_CURRENCIES = ["USDC", "USDT"]

def validate_currency(currency: str) -> int:
    if not currency:
        return 0
    return 1 if currency.upper() in SUPPORTED_CURRENCIES else 0


# -------------------------------
# 🌐 Blockchain Network Validation
# -------------------------------
SUPPORTED_NETWORKS = ["ethereum", "polygon", "solana"]

def validate_network(network: str) -> int:
    if not network:
        return 0
    return 1 if network.lower() in SUPPORTED_NETWORKS else 0


# -------------------------------
# 👛 Wallet Validation (Ethereum style)
# 0x + 40 hex characters
# -------------------------------
def validate_wallet(address: str) -> int:
    if not address:
        return 0

    return 1 if re.fullmatch(r"0x[a-fA-F0-9]{40}", address) else 0


# -------------------------------
# 💵 Amount Validation
# -------------------------------
def validate_amount(amount) -> int:
    try:
        amount = float(amount)
        if amount <= 0:
            return 0
        if amount > 1_000_000:  # Example risk threshold
            return 0
        return 1
    except:
        return 0
