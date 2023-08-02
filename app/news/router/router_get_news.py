from fastapi import Depends, Response

from app.utils import AppModel

from typing import List, Any, Optional, Field

from ..service import Service, get_service
from . import router


class NewsModel(AppModel):
    id: Any = Field(alias="_id")
    url: str
    title: str
    author: str
    published_data: str
    text_list: List[str]
    image_url: str


class GetNewsResponse(AppModel):
    news: List[NewsModel]


@router.get("/", status_code=200, response_model=GetNewsResponse)
def get_news(
    # jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    news_list = svc.repository.get_news()

    return GetNewsResponse(
        news=[
            NewsModel(
                id=news["_id"],
                url=news["url"],
                title=news["title"],
                author=news["author"],
                published_data=news["published_data"],
                text_list=news["text_list"],
                image_url=news["image_url"],
            )
            for news in news_list
        ]
    )
