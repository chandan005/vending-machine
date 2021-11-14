import datetime
import logging
from functools import reduce
from typing import List

from bson.objectid import ObjectId

from app.api.users.models import Role
from app.database.mongodb import db
from app.api.helpers import deps
from app.api.helpers import exceptions
from app.api.auth.security import get_password_hash

logger = logging.getLogger("gunicorn.error")

async def getUserById(id: str): 
    user = await db.vending.users.find_one({"_id": ObjectId(id)})
    if user is None:
        logger.info("Failed to retrieve user [%s]",  id)
        raise exceptions.UserNotFoundException()
    else:
        user = deps.fix_id(user)
        return user

async def createUser(user_payload):
    # Check if user exists with given username
    user_payload["password"] = get_password_hash(password=user_payload["password"])
    user = await db.vending.users.find_one({"username": user_payload.get("username")})
    if user is None:
        # Add Timestamps
        user_payload["created_at"] = datetime.datetime.utcnow()
        user_payload["modified_at"] = datetime.datetime.utcnow()
        
        # Add default deposit of zero for newly created users
        user_payload["deposit"] = 0
        
        user_op = await db.vending.users.insert_one(user_payload)
        if user_op.inserted_id:
            user = await db.vending.users.find_one({"_id": user_op.inserted_id})
            user = deps.fix_id(user)
            return user
        else:
            logger.info("Failed to insert user in db for [%s]",  str(user_payload["username"]))
            raise exceptions.DatabaseException()
    else:
        logger.info("User Exists [%s]",  str(user_payload["username"]))
        raise exceptions.UserExistsException()

# async def updateUser(id, user_payload):
#     user_db = await db.vending.users.find_one({"_id": ObjectId(id)})
#     if user_db is None:
#         logger.info("Failed to retrieve user [%s]",  id)
#         raise exceptions.UserNotFoundException()
#     else:
#         # Username check
#         if "username" in user_payload:
#             username_check = await db.vending.users.find_one({"username": user_payload["username"]})
#             if username_check is not None:
#                 logger.info("user exists")
#                 raise exceptions.UserExistsException()
        
#         user_payload = {**user_db, **user_payload}
#         user_payload["modified_at"] = datetime.datetime.utcnow()

#         user_op = await db.vending.users.update_one({"_id": ObjectId(id)}, {"$set": user_payload})
#         if user_op.modified_count:
#             user = await db.vending.users.find_one({"_id": ObjectId(id)})
#             user = deps.fix_id(user)
#             return user
#         else:
#             logger.info("Failed to update user [%s] while updatigng in db.",  id)
#             raise exceptions.DatabaseException()
        
async def deleteUser(id):
    user = await db.vending.users.find_one({"_id": ObjectId(id)})
    if user is not None:
        if user.get("role") == Role.buyer and user.get("deposit") > 0:
            raise exceptions.DepositExistsBeforeDeletionException()
        
        if user.get("role") == Role.seller:
            seller_has_products = deps.does_seller_have_products(seller_id=user["_id"])
            if seller_has_products:
                raise exceptions.ProductExistsForSellerBeforeDeletionException()
            
        user_op = await db.vending.users.delete_one({"_id": user.get("_id")})
        if user_op.deleted_count:
            return dict()
    else:
        logger.info("Failed to retrieve user [%s]",  id)
        raise exceptions.UserNotFoundException()