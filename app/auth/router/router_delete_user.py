from fastapi import Depends, Response
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from app.trips.service import Service as TripsService
from app.trips.service import get_service as get_trips_service
from . import router
from .dependencies import parse_jwt_user_data


@router.delete("/users/", status_code=200)
def delete_user(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
    trips_svc: TripsService = Depends(get_trips_service)
):
    # trips = svc.repository.get_trips(user_id=jwt_data.user_id)
    svc.repository.delete_user(user_id=jwt_data.user_id)
    # for trip in trips:
        # trips_svc.repository.delete_trip(user_id=jwt_data.user_id, trip_id=trip._id)
    return Response(status_code=200)
