import smtplib
from email.mime.text import MIMEText
import os

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
SMTP_USER = os.getenv("SMTP_USER", "alert@aerodrift.local")
SMTP_PASS = os.getenv("SMTP_PASS", "")

def send_daily_digest(report_data):
    msg = MIMEText(f"AeroDrift Daily Security Digest:\n\n{report_data}")
    msg['Subject'] = 'AeroDrift Daily Report'
    msg['From'] = SMTP_USER
    msg['To'] = 'security-team@aerodrift.local'
    # Mock send for MVP
    print("Mock Email Sent: ", msg['Subject'])
