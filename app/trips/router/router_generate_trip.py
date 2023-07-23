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
    start_date: str
    end_date: str
    num_days: int
    travel_style: str


class GenerateTripResponse(AppModel):
    trip_id: str


@router.post(
    "/generate",
    status_code=status.HTTP_201_CREATED,
    response_model=GenerateTripResponse,
)
def generate_trip(
    input: GenerateTripRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    
    trip_title = input.dict()["trip_title"]
    cities = input.dict()["cities"]
    num_days = str(input.dict()["num_days"])
    travel_style = input.dict()["travel_style"]
    start_date = input.dict()["start_date"]
    end_date = input.dict()["end_date"]
    tags = travel_style.split(", ")
    
    response = svc.openai_service.generate_initial_plan(
        cities=cities, num_days=num_days, travel_style=travel_style
    )

    resp_json = json.loads(response[: len(response) // 2])

    resp_json = svc.google_service.update_photo_references(input_data=resp_json)

    resp_json = svc.s3_service.update_image_urls(
        input_data=resp_json, get_image=svc.google_service.get_image
    )
    trip_id = svc.repository.create_trip(
        trip_title=trip_title,
        user_id=jwt_data.user_id,
        trip_tags=tags,
        start_date=start_date,
        end_date=end_date,
        input=resp_json["trip"],
    )

    return GenerateTripResponse(trip_id=str(trip_id))
