from pydantic import BaseSettings

from app.config import database

from .adapters.jwt_service import JwtService
from .repository.repository import AuthRepository
from .adapters.smtp_service import SMTPService


class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800


config = AuthConfig()


class Service:
    def __init__(
        self,
        repository: AuthRepository,
        jwt_svc: JwtService,
        smtp_svc: SMTPService,
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc
        self.smtp_svc = smtp_svc


def get_service():
    repository = AuthRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
    smtp_svc = SMTPService()

    svc = Service(repository, jwt_svc, smtp_svc=smtp_svc)
    return svc
