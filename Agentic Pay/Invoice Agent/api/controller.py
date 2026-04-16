from fastapi import APIRouter, HTTPException
from summarizeMails import summarize_email
from getEmails import get_recent_emails
import requests
from log_store import logs
router = APIRouter()

#AI_BUYER_AGENT_URL = "http://localhost:8001/buyer/invoice"


@router.get("/")
def invoice_details():
    emails = get_recent_emails()

    invoices = []
    for mail in emails:
        summary = summarize_email(mail)
        invoices.append(summary)

    return {"logs": logs}



