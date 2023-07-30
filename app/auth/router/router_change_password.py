from fastapi import Depends, Response

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data

class changePasswordRequest(AppModel):
    new_password: str

@router.put("/users/password/change", status_code=200)
def change_password(
    input: changePasswordRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> str:
    new_password = input.dict()["new_password"]
    svc.repository.change_password(user_id=jwt_data.user_id, new_password=new_password)
    return Response(status_code=200)
