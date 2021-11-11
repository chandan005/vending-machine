from bson.objectid import ObjectId
from fastapi import HTTPException

from app.database.mongodb import db
from app.api.users.models import Role
from app.api.helpers import exceptions

def fix_id(data):
    data["id"] = str(data["_id"])
    return data

def fix_product_seller_id(data):
    data["id"] = str(data["_id"])
    data["seller_id"] = str(data["seller_id"])
    return data

async def get_product_or_404(id):
    product_cursor = db.vending.products.find({"_id": ObjectId(id)})
    product = await product_cursor.to_list(length=1)
    if len(product) > 0:
        return product[0]
    else:
        raise exceptions.ProductNotFoundException()
    
async def get_product_by_name_or_404(name):
    product_cursor = db.vending.products.find({"product_name": name})
    product = await product_cursor.to_list(length=1)
    if len(product) > 0:
        return product[0]
    else:
        raise exceptions.ProductNotFoundException()
    
async def does_seller_have_products(seller_id):
    products_cursor = db.vending.products.find({"seller_id": ObjectId(seller_id)})
    products = await products_cursor.to_list(length=1)
    if len(products) > 0:
        return True
    else:
        return False

async def get_user_and_check_if_seller(id):
    user = await db.vending.users.find_one({"$and": [{"_id": ObjectId(id), "role": Role.seller}]})
    if user:
        user = fix_id(user)
        return user
    else:
        raise exceptions.SellerDoesNotExistException()

    