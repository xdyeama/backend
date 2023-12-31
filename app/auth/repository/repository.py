from datetime import datetime
from fastapi import HTTPException, Response

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, email: str, password: str):

            payload = {
                "email": email,
                "password": hash_password(password),
                "created_at": datetime.utcnow(),
            }

            self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def edit_user_by_id(self, user_id: str, userData: dict) -> dict | None:
        user = self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "phone": userData["phone"],
                    "name": userData["name"],
                    "city": userData["city"],
                }
            },
        )

        return user

    def change_password(self, user_id: str, password: str):
        self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hash_password(password)}},
        )

    def reset_password(self, email: str, new_password: str):
        user = self.database["users"].find_one({"email": email})
        if user is not None:
            self.database["users"].update_one(
                {"email": email},
                {"$set": {"password": hash_password(new_password)}},
            )

    def delete_user(self, user_id):
        self.database["users"].delete_one({"_id": ObjectId(user_id)})


