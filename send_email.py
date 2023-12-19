import json
import os 
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from termcolor import colored as c

def get_file_names(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return files

with open('credentials.json') as json_file:
    data = json.load(json_file)

# Your email credentials
credentials = data["send_email"]

# Sender email
sender_email = credentials['email']

# Have to use a google "App Password"
# https://myaccount.google.com/apppasswords?utm_source=google-account&utm_medium=myaccountsecurity&utm_campaign=tsv-settings&rapt=AEjHL4OSlufV5eJd3cC76Qm0iMpbc3Trvqaie0N4krStd7uFyWGYZ7bnnZ1jxJpGR22nTj1MAmuoaqCtPWz60Pm96Jqwvu8oU0ND9DquxD_z4LA50ODKT-s
sender_app_password = credentials['password']

# Recipient email address
recipient_email = credentials['recipient_email']

# Create the email 
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email

# Subject of the email 
message["Subject"] = "Test Email with Attachment"

body = "This is a test email with an attachment sent from Python."
message.attach(MIMEText(body, "plain"))

# Get all files from directory 
_path = Path(credentials["file_path"])
attachments = get_file_names(_path)

for attachment in attachments:
    attachment_path = _path / attachment
    
    with open(attachment_path, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {attachment}")
        message.attach(part)

# Connect to the Gmail's SMTP server
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()  # Encrypt the connection
    server.login(sender_email, sender_app_password)
    
    # Send the email
    server.sendmail(sender_email, recipient_email, message.as_string())

print(c("Email sent successfully!", "green"))
