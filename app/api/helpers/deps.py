from datetime import datetime, timedelta
from typing import MutableMapping, List, Union

from bson.objectid import ObjectId
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError

from app.api.helpers.config import settings
from app.database.mongodb import db
from app.api.auth.models import Token, TokenData
from app.api.users.models import Role, UserResponse
from app.api.helpers import exceptions

JWTPayloadMapping = MutableMapping[str, Union[datetime, bool, str, List[str], List[int]]]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_STR}/auth/login")

def fix_id(data):
    data["id"] = str(data["_id"])
    return data

def fix_product_seller_id(data):
    data["id"] = str(data["_id"])
    data["seller_id"] = str(data["seller_id"])
    return data

async def get_user_by_username_or_404(username: str):
    user = await db.vending.users.find_one({"username": username})
    return user
    
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

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,settings.JWT_SECRET,algorithms=[settings.ALGORITHM],options={"verify_aud": False})
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception

    user = await get_user_by_username_or_404(username=token_data.username)
    if user is None:
        raise credentials_exception
    user = fix_id(data=user)
    return user