from fastapi import Depends
from ..service import Service, get_service
from app.auth.service import Service as AuthService
from app.auth.service import get_service as get_auth_service
from . import router
from pydantic import Field
from typing import Any, List, Dict
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


class Trip(AppModel):
    id: Any = Field(alias="_id")
    trip_title: str
    user_id: str
    trip_tags: List[str]
    user_name: str
    user_avatar_url: str
    start_date: str
    end_date: str
    trips: List[Dict]


class GetTripsResponse(AppModel):
    trips: List[Trip]


@router.get("/", status_code=200, response_model=GetTripsResponse)
def get_trips(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
    auth_svc: AuthService = Depends(get_auth_service),
):
    response = svc.repository.get_trips(user_id=jwt_data.user_id)
    user = auth_svc.repository.get_user_by_id(user_id=jwt_data.user_id)
    return GetTripsResponse(
        trips=[
            Trip(
                id=trip["_id"],
                trip_title=trip["trip_title"],
                user_id=str(trip["user_id"]),
                trip_tags=trip["trip_tags"],
                user_name=user["full_name"],
                user_avatar_url=user["avatar_url"],
                start_date=trip["start_date"],
                end_date=trip["end_date"],
                trips=trip["trip"],
            )
            for trip in response
        ]
    )
