import smtplib
from email.message import EmailMessage

import config


def send_otp_email(recipient_email: str, otp: str):
    message = EmailMessage()

    message["Subject"] = "Your Tourist Safety System Verification Code"
    message["From"] = config.SMTP_EMAIL
    message["To"] = recipient_email

    message.set_content(
        f"""
Hello,

Your verification code is:

{otp}

This code will expire in 5 minutes.

If you did not request this code, you can ignore this email.

Regards,
Tourist Safety System
"""
    )

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_EMAIL, config.SMTP_PASSWORD)
        server.send_message(message)