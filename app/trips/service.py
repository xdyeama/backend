from app.config import database
from pydantic import BaseSettings

from .repository.repository import TripsRepository
from .adapters.s3_service import S3Service
from .adapters.google_service import GoogleService

from .adapters.openai_service import LLMService


class Service:
    def __init__(
        self,
        repository: TripsRepository,
        s3_service: S3Service,
        google_service: GoogleService,
        openai_service: LLMService,

    ):
        self.repository = repository
        self.s3_service = s3_service
        self.google_service = google_service
        self.openai_service = openai_service


def get_service():
    repository = TripsRepository(database)
    s3_svc = S3Service()
    google_service = GoogleService()
    openai_service = LLMService()

    svc = Service(repository, s3_svc, google_service, openai_service)

    return svc
