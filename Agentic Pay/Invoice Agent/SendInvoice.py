import requests
from log_store import logs
from PrintData import pretty_log

AI_BUYER_AGENT_URL = "http://localhost:8001/buyer/invoice"

def send_to_buyer_agent(invoice_data: dict):
    #print("inside sendInvoices.py")
    try:
        #print("📤 Sending invoice to AI Buyer Agent...")
        #print(invoice_data)

        pretty_log("Sending invoice to AI Buyer Agent :", invoice_data)

        response = requests.post(
            AI_BUYER_AGENT_URL,
            json=invoice_data,
            timeout=5
        )

        #print("Buyer Agent Response Code:", response.status_code)
        #print("📥 Buyer Agent Response Body:", response.json())

        pretty_log("Ai Buyer Agent Response Body:", response.json())


        logs.append( response.status_code)
        logs.append(response.json())
        

        return response.json()

    except Exception as e:
        print("Failed to send invoice to Buyer Agent:", str(e))
        return None
