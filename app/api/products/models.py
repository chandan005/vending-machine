
import datetime

from typing import Optional
from pydantic import Field, constr, PositiveInt, PositiveFloat

from app.api.helpers.common import BaseModel, PyObjectId


class BaseProduct(BaseModel):
    product_name: Optional[str]
    amount_available: Optional[PositiveInt]
    cost: Optional[PositiveFloat]
    seller_id: PyObjectId =  Field(default_factory=PyObjectId)

class ProductCreate(BaseModel):
    product_name: constr(strip_whitespace=True, min_length=1)
    amount_available: PositiveInt
    cost: PositiveFloat

    class Config:
        schema_extra = {
        "example": {
            "product_name": "Mars",
            "amount_available": 10,
            "cost": 9.99
        }
    }

class ProductModify(BaseModel):
    product_name: Optional[str]
    amount_available: Optional[PositiveInt]
    cost: Optional[PositiveFloat]

    class Config:
        schema_extra = {
            "example": {
                "product_name": "Venus",
                "amount_available": 10,
                "cost": 9.99
        }
    }

class ProductResponse(BaseProduct):
    id: str
    product_name: str
    amount_available: PositiveInt
    cost: PositiveFloat
    seller_id: str
    created_at: datetime.datetime
    modified_at: datetime.datetime
