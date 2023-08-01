from bson.objectid import ObjectId
from pymongo.database import Database
from typing import List, Any
from fastapi import HTTPException


class NewsRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_news(self) -> List[Any] | None:
        news = self.database.news.find()
        return news

    