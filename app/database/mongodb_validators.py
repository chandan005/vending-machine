from bson.objectid import ObjectId
from fastapi import HTTPException
import logging
import datetime

from app.database.monogdb import db
from app.api.users.models import Role
from app.api.helpers import exceptions

async def get_user_or_404(id):
    user = await db.vending.users.find_one({"_id": ObjectId(id)})
    if user:
        return user
    else:
        raise exceptions.UserNotFoundException()

async def get_user_and_check_if_seller(id):
    user = await db.vending.users.find_one({"$and": [{"_id": ObjectId(id), "role": Role.seller}]})
    if user:
        return user
    else:
        raise exceptions.SellerDoesNotExistException()

async def get_product_or_404(id):
    product = await db.vending.products.find_one({"_id": ObjectId(id)})
    if product:
        return product
    else:
        raise exceptions.ProductNotFoundException()

async def get_product_by_seller_or_404(seller_id, product_id):
    
    seller = await get_user_and_check_if_seller(id=seller_id)
    if seller is None:
        raise exceptions.SellerDoesNotExistException()
    
    product = await get_product_or_404(id=product_id)
    
    if product is None:
        raise exceptions.ProductNotFoundException()
    if "seller_id" not in product:
        raise exceptions.ProductDoesNotBelongToSellerException()
    if product.get("seller_id") != seller.get("_id"):
        raise exceptions.ProductDoesNotBelongToSellerException()
    
    return product
    