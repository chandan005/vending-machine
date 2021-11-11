"""MODELS - COMMON
Common variables and base classes for the models
"""

# # Installed # #
import logging
from datetime import datetime
from fastapi import HTTPException
import pydantic
from bson import ObjectId

__all__ = ("BaseModel",)


class BaseModel(pydantic.BaseModel):
    """All data models inherit from this class"""

    @pydantic.root_validator(pre=True)
    def _min_properties(cls, data):
        """At least one property is required"""
        if not data:
            raise ValueError("At least one property is required")
        return data

    def dict(self, include_nulls=False, **kwargs):
        """Override the super dict method by removing null keys from the dict, unless include_nulls=True"""
        kwargs["exclude_none"] = not include_nulls
        return super().dict(**kwargs)

    class Config:
        arbitrary_types_allowed = True
        extra = pydantic.Extra.forbid  # forbid sending additional fields/properties
        anystr_strip_whitespace = True  # strip whitespaces from strings
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

def validate_object_id(id: str):
    try:
        _id = ObjectId(id)
    except Exception:
    	logging.warning("Invalid Object ID")
    	raise HTTPException(status_code=400, detail="Invalid Object ID")
    return _id


def ResponseModel(data):
    return {
        "data": [
            data
        ]
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
    
