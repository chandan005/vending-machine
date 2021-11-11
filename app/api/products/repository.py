import datetime
import logging
from app.api.users.models import Role

from bson.objectid import ObjectId
from fastapi import HTTPException
from typing import List

from app.database.mongodb import db
from app.database import mongodb_validators
from app.api.helpers import exceptions

logger = logging.getLogger("gunicorn.error")

async def getProductById(id):
    product = await db.vending.products.find_one({"_id": ObjectId(id)})
    if product is None:
        logger.info("Failed to retrieve product [%s]",  id)
        raise exceptions.ProductNotFoundException()
    else:
        return product

async def getAllProducts(limit: int = 10, skip: int = 0):
    aggregation = []
    skip_stage = {"$skip": skip}
    limit_stage = {"$limit": limit}
    facet_stage = {
        "$facet": {
            "metadata": [{ "$count": "total_doc_count" }],
            "data": [skip_stage, limit_stage]
        }
    }
    aggregation.append(facet_stage)
    products_cursor = db.vending.products.aggregate(pipeline=aggregation, allowDiskUse=True)
    products = await products_cursor.to_list(length=limit)
    return products
    

async def createProduct(seller_id, product_payload):
    # Check if seller exists with given username
    seller = await db.vending.users.find_one({"$and": [{"_id": ObjectId(seller_id), "role": Role.seller}]})
    if seller is not None:
        
        # Add Timestamps
        product_payload["seller_id"] = ObjectId(seller_id)
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
    seller = await mongodb_validators.get_user_and_check_if_seller(id=seller_id)
    if seller is None:
        raise exceptions.SellerDoesNotExistException()
    else:
        product = await mongodb_validators.get_product_or_404(id=product_id)
        if product is not None:
            if "seller_id" not in product:
                raise exceptions.ProductDoesNotBelongToSellerException()
            else:
                if product.get("seller_id") != seller.get("_id"):
                    raise exceptions.ProductDoesNotBelongToSellerException()
                else:
                    product_payload = {**product, **product_payload}
                    
                    # Add Timestamp
                    product_payload["modified_at"] = datetime.datetime.utcnow()
                    product_op = await db.vending.products.update_one({"_id": ObjectId(id)}, {"$set": product_payload})
                    if product_op.modified_count:
                        user = await db.vending.products.find_one({"_id": ObjectId(id)})
                        return user
                    else:
                        logger.info("Failed to update product [%s] while updatigng in db.",  id)
                        raise exceptions.DatabaseException()
        else:
            raise exceptions.ProductNotFoundException()
    
async def deleteProduct(seller_id, product_id):
    seller = await mongodb_validators.get_user_and_check_if_seller(id=seller_id)
    if seller is None:
        raise exceptions.SellerDoesNotExistException()
    else:
        product = await mongodb_validators.get_product_or_404(id=product_id)
        if product is not None:
            if "seller_id" not in product:
                raise exceptions.ProductDoesNotBelongToSellerException()
            else:
                if product.get("seller_id") != seller.get("_id"):
                    raise exceptions.ProductDoesNotBelongToSellerException()
                else:
                    product_op = await db.vending.products.delete_one({"_id": ObjectId(product_id)})
                    if product_op.deleted_count:
                        return dict()
                    else:
                        raise exceptions.DatabaseException()
        else:
            raise exceptions.ProductNotFoundException()
        
        