import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import os
import re

# --- File paths ---
config_file = r"../input/config.json"
excel_file = r"../data/001.xlsx"
resume_file = r"../input/AdityaKale.pdf"

# --- Read configuration JSON ---
def read_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {file_path}")
        return None

# --- Extract name intelligently ---
def get_dynamic_name(name_field, email_field):
    """Returns proper name if available, else derives from email."""
    name_field = str(name_field).strip() if pd.notna(name_field) else ""
    email_field = str(email_field).strip() if pd.notna(email_field) else ""

    # If name is missing, extract from email
    if not name_field:
        if "@" in email_field:
            extracted = email_field.split("@")[0]
            # Clean up: remove dots, digits, underscores
            extracted = re.sub(r"[\d._-]+", " ", extracted).strip().title()
            if extracted:
                return extracted
        return ""  # fallback
    return name_field.strip().title()

# --- Send email function ---
def send_email(subject: str, body_template: str, excel_path: str, resume_path: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    input_conf = read_json(config_file)
    sender_email = input_conf["email"]
    sender_password = input_conf["token"]

    df = pd.read_excel(excel_path)

    # Ensure required columns
    required_cols = ["Name", "Email", "Status"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    for index, row in df.iterrows():
        receiver_email = str(row["Email"]).strip()
        if not receiver_email or receiver_email.lower() in ["nan", "none"]:
            continue

        status = str(row["Status"]).strip().lower() if pd.notna(row["Status"]) else ""
        if status == "sent":
            continue  # skip already sent

        # Get name dynamically
        name = get_dynamic_name(row["Name"], receiver_email)

        # Dynamic greeting
        greeting = f"Hello {name}," if name else "Hello,"
        personalized_body = body_template.replace("Hello,", greeting)

        try:
            # --- Setup email ---
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(personalized_body, "plain"))

            # --- Attach resume ---
            with open(resume_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(resume_path)}"
                )
                msg.attach(part)

            # --- Send email ---
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            print(f"✅ Sent to {receiver_email} ({name})")
            df.at[index, "Status"] = "Sent"

        except Exception as e:
            print(f"❌ Failed to send to {receiver_email}: {e}")
            df.at[index, "Status"] = f"Failed ({e})"

    # Save Excel with updated status
    df.to_excel(excel_path, index=False)
    print("\n📘 Excel updated with 'Sent' status.")

# --- Run script ---
if __name__ == "__main__":
    config = read_json(config_file)
    subject = config["subject"]
    body = config["body"]

    send_email(subject, body, excel_file, resume_file)
