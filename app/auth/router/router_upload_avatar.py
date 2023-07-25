from fastapi import Depends, Response, UploadFile

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.post("/users/avatar", status_code=200)
def upload_avatar(
    avatar_img: UploadFile,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    auth_svc: Service = Depends(get_service),
):
    avatar_url = auth_svc.s3_service.upload_user_avatar(
        user_id=jwt_data.user_id, file=avatar_img.file, filename=avatar_img.filename
    )
    auth_svc.repository.upload_user_avatar(
        user_id=jwt_data.user_id, avatar_url=avatar_url
    )
    return Response(status_code=200)
