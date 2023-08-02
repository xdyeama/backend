from pymongo.database import Database
from typing import List, Any


class NewsRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_news(self):
        news = self.database.news.find()
        return news
    
    def insert_news(self, news: dict):
        self.database["news"].insert_one(news)

    