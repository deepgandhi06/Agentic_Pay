import imaplib
from config import EMAIL, PASSWORD
from getEmails import get_recent_emails
from summarizeMails import summarize_email
from SendInvoice import send_to_buyer_agent
import time
from log_store import logs



def start_idle_listener():
    #print("👂 Invoice listener started (polling mode)")
    processed_invoice_ids = set()


    while True:
        try:
            #print("inside idle listener.py")
            emails = get_recent_emails(limit=1)

            if not emails:
                print("ℹ️ No unseen invoice mail")
                logs.append("ℹ️ No unseen invoice mail")
                
            else:
                email_data = emails[0]

                print("📩 Invoice mail received")
                print(email_data["sender_email"])
                print(email_data["subject"])

                logs.append("📩 Invoice mail received")
                logs.append(email_data["sender_email"])
                logs.append(email_data["subject"])

                summary = summarize_email(email_data)
                if summary:
                     invoice_id = summary.get("invoice_id")

                     if invoice_id in processed_invoice_ids:
                        print("⚠️ Duplicate invoice detected, skipping...")
                        return

                processed_invoice_ids.add(invoice_id)
                
                logs.append("✅ Invoice processed and sent to AI Buyer Agent")
                send_to_buyer_agent(summary)
                    #print("✅ Invoice processed and sent to AI Buyer Agent")
                    #logs.append("✅ Invoice processed and sent to AI Buyer Agent")

            # 🔑 short wait (NOT 10 minutes)
            time.sleep(20)

        except Exception as e:
            print("⚠️ Listener error:", e)
            time.sleep(30)
