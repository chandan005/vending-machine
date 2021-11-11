from fastapi import APIRouter, Depends, HTTPException, Body, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from .models import *
from .repository import *
from app.api.helpers import exceptions
from app.api.helpers.common import validate_object_id

users_router = APIRouter()

@users_router.post("/", response_model=UserResponse)
async def create(create: UserCreate):
    json_payload = jsonable_encoder(create)
    try:
        user = await createUser(user_payload=json_payload)
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.UserExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return user
    
@users_router.get("/{id}", dependencies=[Depends(validate_object_id)], response_model=UserResponse)
async def read(id: str):
    try:
        user = await getUserById(id=id)
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except exceptions.UserNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    else:
        return user

@users_router.put("/{id}",dependencies=[Depends(validate_object_id)],response_model=UserResponse)
async def update(id: str, modify: UserModify):
    json_payload = jsonable_encoder(modify)
    try:
        user = await updateUser(id=id, user_payload=json_payload)
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.UserNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return user

@users_router.delete("/{id}",dependencies=[Depends(validate_object_id)], response_model=dict)
async def delete(id: str):
    try:
        user = await deleteUser(id=id)
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.UserNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.DepositExistsBeforeDeletionException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return user