import ollama

from SendInvoice import send_to_buyer_agent

import json


def summarize_email(email):
    prompt = f"""
You are an AI assistant that extracts blockchain-based invoice payment details from emails.

IMPORTANT RULES:
- sender_email is already extracted from email headers.
- DO NOT change sender_email.
- DO NOT set sender_email to null.
- Use sender_email exactly as provided.
- If any field (except sender_email) is missing, return null.
- currency should be stablecoin only (USDC | USDT | null).
- network should be blockchain network (ethereum | polygon | solana | null).
- Wallet addresses usually start with 0x if Ethereum-based.

Respond ONLY with valid JSON.
Do NOT add explanations or extra text.

Expected JSON format:
{{
  "sender_email": "{email.get('sender_email')}",
  "invoice_id": "string or null",
  "purpose": "string or null",
  "amount": number or null,
  "currency": "USDC | USDT | null",
  "network": "ethereum | polygon | solana | null",
  "to_wallet": "string or null",
  "due_date": "YYYY-MM-DD or null",
  "transaction_reference": "string or null"
}}

Email Subject:
{email.get('subject')}

Email Body:
{email.get('body')}
"""

    try:
        response = ollama.chat(
            model="llama3.1",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response["message"]["content"]

        parsed_output = json.loads(raw_output)

        # 🔹 Send structured blockchain-ready data
        #send_to_buyer_agent(parsed_output)

        #print("✅ Blockchain invoice extracted and sent to AI Buyer Agent")

        return parsed_output

    except json.JSONDecodeError:
        return {
            "error": "INVALID_JSON_FROM_LLM",
            "sender_email": email.get("sender_email"),
            "raw_response": raw_output
        }

    except Exception as e:
        return {
            "error": "SUMMARIZATION_FAILED",
            "sender_email": email.get("sender_email"),
            "reason": str(e)
        }
