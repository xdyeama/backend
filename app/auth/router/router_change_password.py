from fastapi import Depends, Response

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class ChangePasswordRequest(AppModel):
    password: str


@router.put("/users/password/change", status_code=200)
def change_password(
    input: ChangePasswordRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> str:
    svc.repository.change_password(jwt_data.user_id, input.dict()["password"])

    return Response(status_code=200, detail="Successfully changed password")
