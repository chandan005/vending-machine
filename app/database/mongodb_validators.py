from bson.objectid import ObjectId
from fastapi import HTTPException

from app.database.mongodb import db
from app.api.users.models import Role
from app.api.helpers import exceptions


async def get_user_and_check_if_seller(id):
    user = await db.vending.users.find_one({"$and": [{"_id": ObjectId(id), "role": Role.seller}]})
    if user:
        return user
    else:
        raise exceptions.SellerDoesNotExistException()

    