import datetime
import logging
from functools import reduce
from typing import List

from bson.objectid import ObjectId

from app.api.users.models import Deposit, Role
from app.database.mongodb import db
from app.database import mongodb_validators
from app.api.helpers import exceptions

logger = logging.getLogger("gunicorn.error")

async def getUserById(id: str): 
    user = await db.vending.users.find_one({"_id": ObjectId(id)})
    if user is None:
        logger.info("Failed to retrieve user [%s]",  id)
        raise exceptions.UserNotFoundException()
    else:
        return user

async def createUser(user_payload):
    # Check if user exists with given username
    user = await db.vending.users.find_one({"username": user_payload.get("username")})
    if user is None:
        # Add Timestamps
        user_payload["created_at"] = datetime.datetime.utcnow()
        user_payload["modified_at"] = datetime.datetime.utcnow()
        
        # Add default deposit of zero for newly created users
        user_payload["deposit"] = Deposit.zero
        
        user_op = await db.vending.users.insert_one(user_payload)
        if user_op.inserted_id:
            user = await db.vending.users.find_one({"_id": user_op.inserted_id})
            return user
        else:
            logger.info("Failed to insert user in db for [%s]",  str(user_payload["username"]))
            raise exceptions.DatabaseException()
    else:
        logger.info("User Exists [%s]",  str(user_payload["username"]))
        raise exceptions.UserExistsException()

async def updateUser(id, user_payload):
    user_db = await db.vending.users.find_one({"_id": ObjectId(id)})
    if user_db is None:
        logger.info("Failed to retrieve user [%s]",  id)
        raise exceptions.UserNotFoundException()
    else:
        # Username check
        if "username" in user_payload:
            username_check = await db.vending.users.find_one({"username": user_payload["username"]})
            if username_check is not None:
                logger.info("user exists")
                raise exceptions.UserExistsException()
        
        user_payload = {**user_db, **user_payload}
        user_payload["modified_at"] = datetime.datetime.utcnow()

        user_op = await db.vending.users.update_one({"_id": ObjectId(id)}, {"$set": user_payload})
        if user_op.modified_count:
            user = await db.vending.users.find_one({"_id": ObjectId(id)})
            return user
        else:
            logger.info("Failed to update user [%s] while updatigng in db.",  id)
            raise exceptions.DatabaseException()

async def depositCoin(id: str, coins: List[Deposit]):
    user_db = await db.vending.users.find_one({"_id": ObjectId(id)})
    
    if user_db is None:
        logger.info("Failed to retrieve user [%s]",  id)
        raise exceptions.UserNotFoundException()
    if user_db.get("role") != Role.buyer:
        logger.info("User not buyer [%s]",  id)
        raise exceptions.UserNotBuyerException()
    
    # Get Current deposit for user
    current_deposit = user_db.get("deposit") if "deposit" in user_db else 0
    coins_sum = reduce(lambda a,b:a+b,list(map(int, coins)))
    
    user_payload = user_db
    user_payload["deposit"] = current_deposit + coins_sum
    user_payload["modified_at"] = datetime.datetime.utcnow()
    
    user_op = await db.vending.users.update_one({"_id": ObjectId(id)}, {"$set": user_payload})
    if user_op.modified_count:
        user = await db.vending.users.find_one({"_id": ObjectId(id)})
        return user
    else:
        logger.info("Failed to update user [%s] while updatigng in db.",  id)
        raise exceptions.DatabaseException()
    
async def deleteUser(id):
    user = await db.vending.users.find_one({"_id": ObjectId(id)})
    if user is not None:
        if user.get("deposit") > 0:
            raise exceptions.DepositExistsBeforeDeletionException()

        user_op = await db.vending.users.delete_one({"_id": user.get("_id")})
        if user_op.deleted_count:
            return dict()
    else:
        logger.info("Failed to retrieve user [%s]",  id)
        raise exceptions.UserNotFoundException()