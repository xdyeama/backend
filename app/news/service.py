from app.config import database

from app.news.repository.repository import NewsRepository


class Service:
    def __init__(
        self,
        repository: NewsRepository

    ):
        self.repository = repository


def get_service():
    repository = NewsRepository(database=database)

    svc = Service(repository)

    return svc
