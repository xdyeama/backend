from fastapi import Depends, Response

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data

import os
import smtplib
from email.message import EmailMessage
import secrets


def generate_random_password():
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    new_password = "".join(
        secrets.choice(alphabet) for i in range(10)
    )  # Generate a 10-character random password
    return new_password


def send_reset_password_email(email: str, new_password: str):
    sender_email = os.environ.get(
        "SENDER_EMAIL"
    )  # Replace this with your sender email address
    sender_password = os.environ.get(
        "SENDER_PASS"
    )  # Replace this with your sender email password
    smtp_server = "smtp.gmail.com"  # Replace this with your SMTP server address
    smtp_port = 587  # Replace this with your SMTP port (e.g., 587 for TLS, 465 for SSL)

    msg = EmailMessage()
    msg.set_content(
        f"Your new password for the account with email of {email} is: {new_password}"
    )

    msg["Subject"] = "Password Reset"
    msg["From"] = sender_email
    msg["To"] = email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Password reset email sent.")
    except Exception as e:
        print("Error sending email:", e)


class resetPasswordRequest(AppModel):
    email: str


class resetPasswordResponse(AppModel):
    message: str


@router.put("/users/password/reset", status_code=200)
def reset_password(
    input: resetPasswordRequest,
    svc: Service = Depends(get_service),
) -> str:
    email = input.dict()["email"]
    new_password = generate_random_password()
    user = svc.repository.get_user_by_email(email=email)
    if user is not None:
        svc.repository.reset_password(email=email, new_password=new_password)
        send_reset_password_email(email, new_password)
        return {"message": "Password reset email sent."}
    else:
        return {"message": "User with such email does not exist."}
