from pydantic import BaseModel
from typing import Optional


class InvoiceData(BaseModel):
    # 📧 Email identity
    sender_email: str

    # 🧾 Invoice Details
    invoice_id: Optional[str] = None
    purpose: Optional[str] = None
    due_date: Optional[str] = None

    # 💰 Stablecoin Payment Info
    amount: Optional[float] = None
    currency: Optional[str] = None   # USDC / USDT

    # 🌐 Blockchain Details
    network: Optional[str] = None    # ethereum / polygon / solana
    #from_wallet: Optional[str] = None
    to_wallet: Optional[str] = None

    # 🔎 Optional Reference
    transaction_reference: Optional[str] = None
