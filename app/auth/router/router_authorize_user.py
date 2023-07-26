from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import AppModel

from ..service import Service, get_service
from ..utils.security import check_password
from . import router
from .errors import InvalidCredentialsException


class AuthorizeUserRequest(AppModel):
    email: str
    password: str


class AuthorizeUserResponse(AppModel):
    access_token: str
    token_type: str = "Bearer"


@router.post("/users/tokens", response_model=AuthorizeUserResponse)
def authorize_user(
    # input: OAuth2PasswordRequestForm = Depends(),
    input: AuthorizeUserRequest = Depends(),
    svc: Service = Depends(get_service),
) -> AuthorizeUserResponse:
    # user = svc.repository.get_user_by_email(input.username)
    user = svc.repository.get_user_by_email(input.dict()["email"])
    if not user:
        raise InvalidCredentialsException

    if not check_password(input.dict()["password"], user["password"]):
        raise InvalidCredentialsException

    return AuthorizeUserResponse(
        access_token=svc.jwt_svc.create_access_token(user=user),
    )
