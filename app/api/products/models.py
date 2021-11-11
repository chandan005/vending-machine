
import datetime

from typing import Optional, PositiveInt, PositiveFloat
from pydantic import Field, constr

from app.api.helpers.common import BaseModel, PyObjectId


class BaseProduct(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    productName: Optional[str]
    amountAvailable: Optional[PositiveInt]
    cost: Optional[PositiveFloat]
    sellerId: Field(default_factory=PyObjectId)

class ProductCreate(BaseModel):
    productName: constr(strip_whitespace=True, min_length=1)
    amountAvailable: PositiveInt
    cost: PositiveFloat

    class Config:
        schema_extra = {
        "example": {
            "productName": "Mars",
            "amountAvailable": 10,
            "cost": 9.99
        }
    }

class ProductModify(BaseModel):
    productName: Optional[str]
    amountAvailable: Optional[PositiveInt]
    cost: Optional[PositiveFloat]

    class Config:
        schema_extra = {
            "example": {
                "productName": "Venus",
                "amountAvailable": 10,
                "cost": 9.99
        }
    }

class ProductInDB(BaseProduct):
    pass

class ProductResponse(BaseProduct):
    id: PyObjectId
    amountAvailable: PositiveInt
    cost: PositiveFloat
    sellerId: PyObjectId
    created_at: datetime.datetime
    modified_at: datetime.datetime
    pass
