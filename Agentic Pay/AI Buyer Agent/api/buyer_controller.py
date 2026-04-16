
from models.invoice import InvoiceData
from processor import process_invoice_data
# api/buyer_controller.py
from fastapi import APIRouter, HTTPException

# Create the router (define BEFORE using it)
router = APIRouter(prefix="/buyer", tags=["buyer"])

@router.post("/invoice")
async def receive_invoice(invoice: InvoiceData):
    print("✅ Invoice received in AI-Buyer Agent")
    print(invoice.model_dump())  # Pydantic v2

    try:
        result = process_invoice_data(invoice)
    except Exception as e:
        # surface processor errors as 400/500 depending on your context
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

    return {
        "status": result.get("status", "unknown"),
        "result": result
    }