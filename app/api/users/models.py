
import datetime
from enum import Enum
from typing import Optional

from pydantic import Field, constr

from app.api.helpers.common import BaseModel

class Role(str, Enum):
    """[summary]
        Used to manage user type.
    [description]
        Simple enumeration to link the user type.
    """
    seller = "seller"
    buyer = "buyer"

class Deposit(int, Enum):
    """[summary]
        Allowed deposit types.
    [description]
        Simple enumeration to check for allowed deposit types.
    """
    five = 5
    ten = 10
    twenty = 20
    fifty = 50
    hundred = 100

class BaseUser(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[Role]
    deposit: Optional[int]

class UserCreate(BaseModel):
    username: constr(strip_whitespace=True, min_length=5)
    password: constr(strip_whitespace=True, min_length=8)
    role: Role = Field(Role.buyer)

    class Config:
        schema_extra = {
            "example": {
                "username": "chandansingh005",
                "password": "asdfghjk",
                "role": Role.buyer
            }
        }

class UserModify(BaseModel):
    username: Optional[constr(strip_whitespace=True, min_length=5)]

    class Config:
        schema_extra = {
            "example": {
                "username": "chandansingh005"
            }
        }

class UserResponse(BaseModel):
    id: str
    username: str
    role: Role
    deposit: int
    created_at: datetime.datetime
    modified_at: datetime.datetime

    