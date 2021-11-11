from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from .models import *
from .repository import *
from app.api.helpers import exceptions
from app.api.helpers.common import validate_object_id

transactions_router = APIRouter()

@transactions_router.post("/deposit/{user_id}",response_model=UserResponse)
async def deposit(user_id: str, payload: DepositCoin):
    json_payload = jsonable_encoder(payload)
    coins = list(map(int, json_payload.get("coins")))
    try:
        deposit = await depositCoin(user_id=user_id, coins=coins)
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.UserNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.UserNotBuyerException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return deposit

@transactions_router.post("/buy/{id}",response_model=PurchasedTransaction)
async def deposit(user_id: str, payload: BuyProduct):
    json_payload = jsonable_encoder(payload)
    try:
        transaction = await buyProduct(user_id=user_id, product_id=json_payload.get("product_id"), product_amount=json_payload.get("amount"))
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.UserNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.ProductNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.ProductStockUnavailableException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.UserInSufficientDepositException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return transaction