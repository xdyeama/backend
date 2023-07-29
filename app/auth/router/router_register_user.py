from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class RegisterUserRequest(AppModel):
    email: str
    password: str


class RegisterUserResponse(AppModel):
    email: str


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse
)
def register_user(
    input: RegisterUserRequest,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    if svc.repository.get_user_by_email(input.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already taken.",
        )
    print(input)
    svc.repository.create_user(email=input.email, password=input.password)

    return RegisterUserResponse(email=input.email)
