import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import router as api_router
from app.api.helpers.config import settings
from app.database.mongodb_utils import close_mongo_connection, connect_to_mongo


app = FastAPI(title="Vending Machine API", openapi_url=f"{settings.API_STR}/openapi.json")
logger = logging.getLogger("gunicorn.error")

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_startup():
    logger.info("Request Started.")
    await connect_to_mongo()

@app.on_event("shutdown")
async def app_shutdown():
    logger.info("Request Ended.")
    await close_mongo_connection()

@app.get("/", tags=["Health Check"])
async def read_root():
    return {"message": "Welcome to Vending Machine app!"}


app.include_router(api_router, prefix=settings.API_STR)
