import requests
from urllib.parse import urlsplit, parse_qsl
import json
import os


class GoogleService:
    def __init__(self):
        self.gplaces_api_key = os.environ.get("GPLACES_API_KEY")
        self.places_data_path = "./data/places_data.json"

    def update_photo_references(self, input_data):
        day_plans = input_data["trip"]
        places = [
            "museums",
            "restaurants",
            "cafes",
            "theaters",
            "sport complexes",
            "shopping centers",
        ]
        with open(self.places_data_path, "r") as f:
            places_data = json.load(f)
            cities = places_data["cities"]

            for day_id, day in enumerate(day_plans):
                activities = day["activities"]
                for activity_id, activity in enumerate(activities):
                    isPhotoRefExist = False
                    isLocationExist = False
                    isRatingExist = False
                    isTypesExist = False
                    place_name = activity["place_name"]
                    city_name = day["city"]

                    for city in cities:
                        if city["city_name"] == city_name:
                            for place in places:
                                for place_elem in city[place]:
                                    if place_elem["name"] == place_name:
                                        input_data["trip"][day_id]["activities"][
                                            activity_id
                                        ]["coordinates"] = place_elem["geometry"][
                                            "location"
                                        ]
                                        isLocationExist = True

                                        input_data["trip"][day_id]["activities"][
                                            activity_id
                                        ]["rating"] = place_elem["rating"]
                                        input_data["trip"][day_id]["activities"][
                                            activity_id
                                        ]["rating_count"] = place_elem[
                                            "user_ratings_total"
                                        ]
                                        isRatingExist = True

                                        input_data["trip"][day_id]["activities"][
                                            activity_id
                                        ]["activity_types"] = place_elem["types"]
                                        isTypesExist = True

                                        if "photos" in place_elem:
                                            photos = place_elem["photos"]
                                            if photos:
                                                input_data["trip"][day_id][
                                                    "activities"
                                                ][activity_id]["photo_ref"] = photos[0][
                                                    "photo_reference"
                                                ]
                                                isPhotoRefExist = True
                    if not isPhotoRefExist:
                        input_data["trip"][day_id]["activities"][activity_id][
                            "photo_ref"
                        ] = ""
                    if not isLocationExist:
                        input_data["trip"][day_id]["activities"][activity_id][
                            "coordinates"
                        ] = {
                            "lat": 48.0196,
                            "lng": 66.9237
                        }
                    if not isRatingExist:
                        input_data["trip"][day_id]["activities"][activity_id][
                            "rating"
                        ] = 0
                        input_data["trip"][day_id]["activities"][activity_id][
                            "rating_count"
                        ] = 0
                    if not isTypesExist:
                        input_data["trip"][day_id]["activities"][activity_id][
                            "activity_types"
                        ] = []

                    isPhotoRefExist = False
                    isLocationExist = False
                    isRatingExist = False
                    isTypesExist = False
            return input_data

    def get_image(self, photo_reference: str):
        url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={self.gplaces_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None
