import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
from bs4 import BeautifulSoup
from config import EMAIL, PASSWORD


def get_recent_emails(limit=1):
   # print("inside getEmails.py")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # ONLY unseen invoice mails
    status, messages = mail.search(None, '(UNSEEN SUBJECT "Invoice")')

    if status != "OK" or not messages[0]:
        return []

    # Respect limit (limit = 1)
    email_ids = messages[0].split()[:limit]

    emails = []

    for e_id in email_ids:
        # fetch() marks mail as SEEN
        _, msg_data = mail.fetch(e_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # -------- Subject --------
        subject, encoding = decode_header(msg.get("Subject"))[0]
        subject = subject.decode(encoding) if isinstance(subject, bytes) else subject

        # -------- Sender Email --------
        from_header = msg.get("From")
        sender_email = None

        if from_header:
            decoded_from, enc = decode_header(from_header)[0]
            decoded_from = (
                decoded_from.decode(enc) if isinstance(decoded_from, bytes) else decoded_from
            )
            _, sender_email = parseaddr(decoded_from)

        # -------- Body --------
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    soup = BeautifulSoup(
                        part.get_payload(decode=True), "html.parser"
                    )
                    body = soup.get_text()
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        emails.append({
            "email_id": e_id.decode(),
            "sender_email": sender_email,
            "subject": subject,
            "body": body[:2000]
        })

    return emails
