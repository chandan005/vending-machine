
from typing import List
from pydantic import Field, PositiveFloat, PositiveInt

from app.api.helpers.common import BaseModel
from app.api.users.models import Deposit
from app.api.products.models import ProductResponse

class DepositCoin(BaseModel):
    coins: List[Deposit]
    
    class Config:
        schema_extra = {
            "example": {
                "coins": [Deposit.five, Deposit.ten]
            }
        }

class BuyProduct(BaseModel):
    product_id: str
    amount: PositiveInt
    
    class Config:
        schema_extra = {
            "example": {
                "product_id": "1",
                "amount": 10
            }
        }
    
class PurchasedProduct(BaseModel):
    product_name: str
    amount_bought: PositiveInt
    unit_price: PositiveFloat
    
class PurchasedTransaction(BaseModel):
    total_spent: float
    product: PurchasedProduct
    change: List[Deposit]