from fastapi import APIRouter, Depends, HTTPException, Body, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from .models import *
from .repository import *
from app.api.helpers import exceptions
from app.api.helpers.common import validate_object_id
from app.api.helpers.deps import get_current_user

products_router = APIRouter()

@products_router.post("/", dependencies=[Depends(get_current_user)], response_model=ProductResponse)
async def create(seller_id: str, create: ProductCreate):
    json_payload = jsonable_encoder(create)
    try:
        product = await createProduct(seller_id = seller_id, product_payload=json_payload)
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.SellerDoesNotExistException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return product
    
@products_router.get("/{id}", dependencies=[Depends(validate_object_id)], response_model=ProductResponse)
async def read(id: str):
    try:
        product = await getProductById(id=id)
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except exceptions.ProductNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    else:
        return product

@products_router.get("/", response_model=List[ProductResponse])
async def read_all():
    try:
        products = await getAllProducts()
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    else:
        return products

@products_router.put("/", dependencies=[Depends(get_current_user)], response_model=ProductResponse)
async def update(product_id: str, seller_id: str,  modify: ProductModify):
    json_payload = jsonable_encoder(modify)
    try:
        product = await updateProduct(seller_id=seller_id, product_id=product_id, product_payload=json_payload)
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.ProductNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.ProductDoesNotBelongToSellerException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return product

@products_router.delete("/", dependencies=[Depends(get_current_user)], response_model=dict)
async def delete(product_id: str, seller_id: str):
    try:
        product = await deleteProduct(seller_id=seller_id, product_id=product_id)
    except exceptions.DatabaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.ProductNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except exceptions.ProductDoesNotBelongToSellerException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return product