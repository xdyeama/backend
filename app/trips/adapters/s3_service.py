from typing import BinaryIO
from io import BytesIO
import botocore
import boto3


class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket_name = "sayahatai"
        self.bucket_location = boto3.client("s3").get_bucket_location(
            Bucket=self.bucket_name
        )

    def upload_image(self, city: str, image, place_name: str):
        place_name = place_name.lower().replace(" ", "_")
        filekey = f"places/{city}/{place_name}.png"

        self.s3.upload_fileobj(BytesIO(image), self.bucket_name, filekey)

        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            self.bucket_location["LocationConstraint"], self.bucket_name, filekey
        )
        return object_url

    def check_file_exists(self, city: str, place_name: str):
        filekey = f"places/{city}/{place_name}.png"
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=filekey)
            return True
        except Exception:
            return False

    def load_image_from_s3(self, bucket_name, key):
        s3 = boto3.resource("s3")
        try:
            obj = s3.Object(bucket_name, key)
            image_data = obj.get()["Body"].read()
            return image_data
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                print("The object does not exist.")
            else:
                print("An error occurred while loading the image.")

        return None

    def update_image_urls(self, input_data, get_image):
        day_plans = input_data["trip"]

        for day_plan_id, day_plan in enumerate(day_plans):
            city = day_plan["city"]
            activities = day_plan["activities"]
            for activity_id, activity in enumerate(activities):
                place_name = activity["place_name"]
                photo_ref = activity["photo_ref"]
                if photo_ref != "":
                    # if self.check_file_exists(city=city, photo_ref=photo_ref):
                    #     image_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
                    #         self.bucket_location["LocationConstraint"],
                    #         self.bucket_name,
                    #         f"places/{city}/{photo_ref}.png",
                    #     )
                    # else:
                    image_url = self.upload_image(
                        city=city, place_name=place_name, image=get_image(photo_ref)
                    )
                    input_data["trip"][day_plan_id]["activities"][activity_id][
                        "image_url"
                    ] = image_url
                else:
                    input_data["trip"][day_plan_id]["activities"][activity_id][
                        "image_url"
                    ] = ""

        return input_data
