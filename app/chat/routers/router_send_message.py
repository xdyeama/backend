from fastapi import Depends, status, Response

from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


from ..service import Service, get_service
from . import router

import json


class GenerateTripRequest(AppModel):
    trip_title: str
    cities: str
    num_days: int
    travel_style: str




@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
)
def generate_trip(
    input: GenerateTripRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    
    trip_title = input.dict()["trip_title"]
    cities = input.dict()["cities"]
    num_days = input.dict()["num_days"]
    travel_style = input.dict()["travel_style"]
    tags = travel_style.split(", ")

    response = svc.openai_service.generate_initial_plan(
        cities=cities, num_days=str(num_days), travel_style=travel_style
    )

    resp_json = json.loads(response[: len(response) // 2])

    return Response(status_code=200)
