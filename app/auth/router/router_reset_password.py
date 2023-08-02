from fastapi import Depends, Response

from app.utils import AppModel

from ..service import Service, get_service
from . import router
from email.message import EmailMessage
import secrets


def generate_random_password():
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    new_password = "".join(
        secrets.choice(alphabet) for i in range(10)
    )  # Generate a 10-character random password
    return new_password


class ResetPasswordRequest(AppModel):
    email: str


@router.put(
    "/users/password/reset", status_code=200
)
def reset_password(
    input: ResetPasswordRequest,
    svc: Service = Depends(get_service),
) -> str:
    email = input.dict()["email"]
    new_password = generate_random_password()
    user = svc.repository.get_user_by_email(email=email)
    if user is not None:
        svc.repository.reset_password(email=email, new_password=new_password)
        svc.smtp_svc.send_new_password_email(email, new_password=new_password)
        return Response(status_code=200)
    else:
        return Response(status_code=404)
