from fastapi import APIRouter

from .auth.routes import auth_router
from .users.routes import users_router
from .products.routes import products_router
from .transactions.routes import transactions_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(products_router, prefix="/products", tags=["Products"])
router.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])