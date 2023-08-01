from fastapi import Depends, Response

from app.utils import AppModel

from typing import List, Any, Optional

from ..service import Service, get_service
from . import router
from app.jobs.tasks import scrape_news


@router.post(
    "/",
    status_code=200,
    # response_model=GetNewsResponse
)
def insert_news(
    # jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, list]:
    scrape_news()
    return Response(status_code=200)
