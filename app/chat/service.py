from app.config import database
from pydantic import BaseSettings

from .adapters.openai_service import LLMService


class Service:
    def __init__(
        self,
        repository: TripsRepository,
        openai_service: LLMService,

    ):
        self.openai_service = openai_service


def get_service():
    openai_service = LLMService()

    svc = Service(repository, openai_service)

    return svc
