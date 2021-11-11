from fastapi import APIRouter

from .users.routes import users_router
from .products.routes import products_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(products_router, prefix="/products", tags=["Products"])