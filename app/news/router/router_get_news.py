from fastapi import Depends

from app.utils import AppModel


from typing import List, Any

from ..service import Service, get_service
from . import router


class GetNewsResponse(AppModel):
    news: List(Any)


@router.get(
    "/",
    status_code=200,
    response_model=GetNewsResponse
)
def get_news(
    # jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    
    news_list = svc.repository.get_news()

    return GetNewsResponse(news=news_list)
