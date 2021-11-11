import datetime
import logging
from app.api.users.models import Role

from bson.objectid import ObjectId
from fastapi import HTTPException

from app.database.mongodb import db
from app.api.helpers import exceptions

logger = logging.getLogger("gunicorn.error")

async def getProductById(id):
    product = await db.vending.products.find_one({"_id": ObjectId(id)})
    if product is None:
        logger.info("Failed to retrieve product [%s]",  id)
        raise exceptions.UserNotFoundException()
    else:
        return product

async def createProduct(seller_id, product_payload):
    # Check if seller exists with given username
    seller = await db.vending.users.find_one({"$and": [{"_id": ObjectId(seller_id), "role": Role.seller}]})
    if seller is not None:
        
        # Add Timestamps
        product_payload["created_at"] = datetime.datetime.utcnow()
        product_payload["modified_at"] = datetime.datetime.utcnow()
        
        product_op = await db.vending.products.insert_one(product_payload)
        if product_op.inserted_id:
            prodcut = await db.vending.products.find_one({"_id": product_op.inserted_id})
            return prodcut
        else:
            logger.info("Failed to insert product in db for")
            raise exceptions.DatabaseException()
    else:
        logger.info("Seller Does not Exist [%s]",  str(seller_id))
        raise exceptions.SellerDoesNotExistException()

async def updateProduct(seller_id, product_id, product_payload):
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
    
async def deleteProduct(seller_id, product_id):
    user = await db.vending.users.find_one({"_id": ObjectId(id_)})
    if user is not None:
        if user.get("deposit") > 0:
            raise exceptions.DepositExistsBeforeDeletionException()

        feed_op = await db.vending.feeds.delete_one({"_id": user.get("_id")})
        if feed_op.deleted_count:
            return dict()
    else:
        logger.info("Failed to retrieve user [%s]",  id)
        raise exceptions.UserNotFoundException()