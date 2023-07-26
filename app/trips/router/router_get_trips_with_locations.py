from fastapi import Depends
from ..service import Service, get_service
from . import router
from pydantic import Field
from typing import Any, List, Dict
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


class Location(AppModel):
    place_name: str
    city: str
    description: str
    coordinates: dict | None
    website: str | None
    image_url: List[str]


class TripModel(AppModel):
    id: Any = str
    trip_title: str
    locations: List[Location]


class GetTripLocationsResponse(AppModel):
    trips: List[TripModel]


@router.get("/locations/", status_code=200, response_model=GetTripLocationsResponse)
def get_trips_with_locations(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    response = svc.repository.get_trips_with_locations(user_id=jwt_data.user_id)
    return GetTripLocationsResponse(trips=response)
