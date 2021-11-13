import datetime
import logging
from app.api.users.models import Role

from bson.objectid import ObjectId
from fastapi import HTTPException
from typing import List

from app.database.mongodb import db
from app.api.helpers import deps
from app.api.helpers import exceptions

logger = logging.getLogger("gunicorn.error")

async def getProductById(id):
    product = await db.vending.products.find_one({"_id": ObjectId(id)})
    if product is None:
        logger.info("Failed to retrieve product [%s]",  id)
        raise exceptions.ProductNotFoundException()
    else:
        product = deps.fix_product_seller_id(product)
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
    return list(map(deps.fix_product_seller_id, products))
    

async def createProduct(seller_id, product_payload):
    
    # Check if seller exists with given username
    seller = await db.vending.users.find_one({"$and": [{"_id": ObjectId(seller_id), "role": Role.seller}]})
    if seller is not None:
        try:
            existing_product_db = await deps.get_product_by_name_or_404(name=product_payload["product_name"])
            product_payload["modified_at"] = datetime.datetime.utcnow()
            product_payload["amount_available"] = existing_product_db.get("amount_available") + product_payload.get("amount_available")
            product_op = await db.vending.products.update_one({"_id": ObjectId(existing_product_db["_id"])}, {"$set": product_payload})
            if product_op.modified_count:
                product = await db.vending.products.find_one({"_id": ObjectId(existing_product_db["_id"])})
                product = deps.fix_product_seller_id(product)
                return product
            else:
                logger.info("Failed to update product [%s] while updatigng in db.",  existing_product_db["_id"])
                raise exceptions.DatabaseException()
            
        except exceptions.ProductNotFoundException as e:
            # Add Timestamps
            product_payload["seller_id"] = ObjectId(seller_id)
            product_payload["created_at"] = datetime.datetime.utcnow()
            product_payload["modified_at"] = datetime.datetime.utcnow()
            
            product_op = await db.vending.products.insert_one(product_payload)
            if product_op.inserted_id:
                product = await db.vending.products.find_one({"_id": product_op.inserted_id})
                product = deps.fix_product_seller_id(product)
                return product
            else:
                logger.info("Failed to insert product in db for")
                raise exceptions.DatabaseException()
    else:
        logger.info("Seller Does not Exist [%s]",  str(seller_id))
        raise exceptions.SellerDoesNotExistException()

async def updateProduct(seller_id, product_id, product_payload):
    seller_db = await deps.get_user_and_check_if_seller(id=seller_id)
    if seller_db is None:
        raise exceptions.SellerDoesNotExistException()
    else:
        product_db = await deps.get_product_or_404(id=product_id)
        if product_db is not None:
            if "seller_id" not in product_db:
                raise exceptions.ProductDoesNotBelongToSellerException()
            else:
                if product_db.get("seller_id") != seller_db.get("_id"):
                    raise exceptions.ProductDoesNotBelongToSellerException()
                else:
                    product_payload = {**product_db, **product_payload}
                    
                    # Add Timestamp
                    product_payload["modified_at"] = datetime.datetime.utcnow()
                    product_op = await db.vending.products.update_one({"_id": ObjectId(product_id)}, {"$set": product_payload})
                    if product_op.modified_count:
                        product = await db.vending.products.find_one({"_id": ObjectId(product_id)})
                        product = deps.fix_product_seller_id(product)
                        return product
                    else:
                        logger.info("Failed to update product [%s] while updatigng in db.",  product_id)
                        raise exceptions.DatabaseException()
        else:
            raise exceptions.ProductNotFoundException()
    
async def deleteProduct(seller_id, product_id):
    seller = await deps.get_user_and_check_if_seller(id=seller_id)
    if seller is None:
        raise exceptions.SellerDoesNotExistException()
    else:
        product = await deps.get_product_or_404(id=product_id)
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
        
        