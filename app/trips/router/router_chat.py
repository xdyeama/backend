from fastapi import Depends

from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


from ..service import Service, get_service
from . import router


class ChatRequest(AppModel):
    question: str


class ChatResponse(AppModel):
    answer: str


@router.post(
    "/chat",
    status_code=200,
    response_model=ChatResponse
)
def chat_with_model(
    input: ChatRequest,
    # jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    
    question = input.dict()["question"]
    answer = svc.openai_service.chat_with_model(question=question)

    return ChatResponse(answer=answer)
