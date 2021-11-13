import datetime
import logging
from functools import reduce
from typing import List

from bson.objectid import ObjectId

from app.api.users.models import Deposit, Role
from app.database.mongodb import db
from app.api.helpers import deps
from app.api.helpers import exceptions

logger = logging.getLogger()

def change_notes(change, coins):
    coins_out = []
    if min(coins) > change:
        return coins_out
    
    n = len(coins)
    
    # Traverse through all denomination
    i = n - 1
    while(i >= 0):
        # Find denominations
        while (change >= coins[i]):
            change -= coins[i]
            coins_out.append(coins[i])
        i -= 1
    return coins_out

async def depositCoin(user_id: str, coins: List[Deposit]):
    user_db = await db.vending.users.find_one({"_id": ObjectId(user_id)})
    
    if user_db is None:
        logger.info("Failed to retrieve user [%s]",  user_id)
        raise exceptions.UserNotFoundException()
    if user_db.get("role") != Role.buyer:
        logger.info("User not buyer [%s]",  user_id)
        raise exceptions.UserNotBuyerException()
    
    # Get Current deposit for user
    current_deposit = user_db.get("deposit") if "deposit" in user_db else 0
    coins_sum = reduce(lambda a,b:a+b,list(map(int, coins)))
    
    user_payload = user_db
    user_payload["deposit"] = current_deposit + coins_sum
    user_payload["modified_at"] = datetime.datetime.utcnow()
    
    user_op = await db.vending.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_payload})
    if user_op.modified_count:
        user = await db.vending.users.find_one({"_id": ObjectId(user_id)})
        user = deps.fix_id(user)
        return user
    else:
        logger.info("Failed to update user [%s] while updatigng in db.",  user_id)
        raise exceptions.DatabaseException()

async def buyProduct(user_id: str, product_id: str, product_amount: int):
    user_db = await db.vending.users.find_one({"_id": ObjectId(user_id)})
    
    if user_db is None:
        logger.info("Failed to retrieve user [%s]",  user_id)
        raise exceptions.UserNotFoundException()
    if user_db.get("role") != Role.buyer:
        logger.info("User not buyer [%s]",  user_id)
        raise exceptions.UserNotBuyerException()
    try:
        product_db = await deps.get_product_or_404(id=product_id)
    except exceptions.ProductNotFoundException as e:
        raise exceptions.ProductNotFoundException()
    else:
        # Check if product stock available
        if product_db.get("amount_available") >= product_amount:
            
            # Get Current deposit for user
            current_deposit = user_db.get("deposit") if "deposit" in user_db else 0
            if current_deposit == 0:
                raise exceptions.UserInSufficientDepositException("User currently has 0 coins deposited.")
            
            # Check if current deposit is valid to buy products
            cost_of_product_in_cents = product_db.get("cost") * 100
            total_price_of_products = cost_of_product_in_cents * product_amount
            
            if current_deposit >= total_price_of_products:
                user_payload = user_db
                user_payload["deposit"] = current_deposit - total_price_of_products
                user_payload["modified_at"] = datetime.datetime.utcnow()
                user_op = await db.vending.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_payload})
                if not user_op.modified_count:
                    logger.info("Failed to update user [%s] while updatigng in db.",  user_id)
                    raise exceptions.DatabaseException()


                product_payload = product_db
                product_payload["amount_available"] = product_db.get("amount_available") - product_amount
                product_payload["modified_at"] = datetime.datetime.utcnow()
                product_op = await db.vending.products.update_one({"_id": ObjectId(product_id)}, {"$set": product_payload})
                if not product_op.modified_count:
                    logger.info("Failed to update product [%s] while updatigng in db.",  product_id)
                    raise exceptions.DatabaseException()

                puchased_product = {
                    "product_name": product_db.get("product_name"),
                    "amount_bought": product_amount,
                    "unit_price": product_db.get("cost")
                }
                transaction = {
                    "total_spent": float(cost_of_product_in_cents / 100),
                    "product": puchased_product,
                    "change": change_notes(change=current_deposit, coins=list(map(int, Deposit)))
                }
                return transaction
            else:
                raise exceptions.UserInSufficientDepositException()
        else:
            raise exceptions.ProductStockUnavailableException()
        
async def resetDeposit(user_id: str):
    user_db = await db.vending.users.find_one({"_id": ObjectId(user_id)})
    
    if user_db is None:
        logger.info("Failed to retrieve user [%s]",  user_id)
        raise exceptions.UserNotFoundException()
    if user_db.get("role") != Role.buyer:
        logger.info("User not buyer [%s]",  user_id)
        raise exceptions.UserNotBuyerException()
    
    user_payload = user_db
    user_payload["deposit"] = 0
    user_payload["modified_at"] = datetime.datetime.utcnow()
    user_op = await db.vending.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_payload})
    if user_op.modified_count:
        user = await db.vending.users.find_one({"_id": ObjectId(user_id)})
        user = deps.fix_id(user)
        return user
    else:
        logger.info("Failed to update user [%s] while updatigng in db.",  user_id)
        raise exceptions.DatabaseException()