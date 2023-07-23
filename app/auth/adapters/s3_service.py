from typing import BinaryIO
from io import BytesIO


import boto3


class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket_name = "sayahatai"
        self.bucket_location = boto3.client("s3").get_bucket_location(
            Bucket=self.bucket_name
        )

    def upload_user_avatar(self, user_id: str, file):
        filekey = f"users/{user_id}/avatar.png"

        self.s3.upload_fileobj(BytesIO(file), self.bucket_name, filekey)

        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            self.bucket_location["LocationConstraint"], self.bucket_name, filekey
        )
        return object_url

    def update_user_avatar(self, user_id: str, file: BinaryIO):
        filekey = f"users/{user_id}/avatar.png"
        self.delete_avatar(user_id=user_id)
            
        self.s3.upload_fileobj(file, self.bucket_name, filekey)

        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            self.bucket_location["LocationConstraint"], self.bucket_name, filekey
        )
        return object_url

    def delete_avatar(self, user_id: str):
        filekey = f"users/{user_id}/avatar.png"

        self.s3.delete_object(Bucket=self.bucket_name, Key=filekey)
