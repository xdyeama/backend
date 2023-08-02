import os
from email.message import EmailMessage
import ssl
import smtplib


class SMTPService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.email_sender = os.environ.get("EMAIL_SENDER")
        self.email_password = os.environ.get("EMAIL_PASS")
        self.subject = "New password request from {email}"
        self.body = """You have requested new password to login into Sayahat.AI app. 
        Your new password for the email {email} is {new_password}"""
        self.ssl_context = ssl.create_default_context()

    def send_new_password_email(self, email, new_password):
        email_subject = self.subject.format(email=email)

        email_message = EmailMessage()
        email_message["From"] = self.email_sender
        email_message["To"] = email
        email_message["Subject"] = email_subject
        email_message.set_content(
            self.body.format(email=email, new_password=new_password)
        )

        with smtplib.SMTP(self.smtp_server, 587) as smtp:
            # with smtplib.SMTP_SSL(self.smtp_server, 465, self.ssl_context) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.email_sender, self.email_password)
            smtp.sendmail(self.email_sender, email, email_message.as_string())
