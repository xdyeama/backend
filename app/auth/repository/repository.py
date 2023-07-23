from datetime import datetime
from fastapi import HTTPException

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "full_name": user["full_name"],
            "email": user["email"],
            "avatar_url": "",
            "password": hash_password(user["password"]),
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

    def delete_user(self, user_id):
        self.database["users"].delete({"_id": ObjectId(user_id)})

    def upload_avatar(self, user_id: str, avatar_url: str):
        self.database["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"avatar_url": avatar_url}}
        )

    def delete_avatar(self, user_id: str):
        user = self.database["users"].find_one({"_id": ObjectId(user_id)})
        if user["avatar_url"]:
            self.database["users"].update_one(
                {"_id": ObjectId(user_id)}, {"$set": {"avatar_url": ""}}
            )
        else:
            raise HTTPException(status_code=404, detail="No avatar image to delete")
