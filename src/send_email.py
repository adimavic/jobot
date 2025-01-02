import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json


# Function to fetch content from a URL
config_file = rf"../input/config.json"
querry_file = rf"../input/querry.json"


def read_json(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as config:
            configuration = json.load(config)
        return configuration
    except FileNotFoundError:
        print(f"File not found: {config_file}")
        return None

# Function to send email with attachment
def send_email(subject: str, body: str, excel_file: str, resume_file: str):
    # Gmail SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    input_conf = read_json(config_file)
    # Your Gmail account credentials
    sender_email = input_conf['email']
    sender_password = input_conf['token']  # Use your App Password if 2FA is enabled

    # Load email addresses from the Excel file
    df = pd.read_excel(excel_file)
    recipient_emails = df['Email'].tolist()

    # Loop through each recipient and send the email
    for receiver_email in recipient_emails:
        try:
            # Email Headers
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Email Body
            msg.attach(MIMEText(body, 'plain'))

            # Attach the Resume
            attachment = open(resume_file, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {resume_file.split('/')[-1]}")
            msg.attach(part)

            # Set up the SMTP server and login
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            server.send_message(msg)
            print(f"Email sent successfully to {receiver_email}")

            # Close the attachment
            attachment.close()
            server.quit()

        except Exception as e:
            print(f"Failed to send email to {receiver_email}: {e}")

# Email details
input_conf = read_json(config_file)
subject = input_conf['subject']
body = input_conf['body']

# Input files
excel_file = rf"../output/email_list.xlsx"
resume_file = rf"../input/AdityaKaleResume.pdf"  # Path to your resume PDF

# Call the function
send_email(subject, body, excel_file, resume_file)
