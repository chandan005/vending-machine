import logging
import os

from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db

async def connect_to_mongo():
    logging.info("Connecting to MongoDB...")
    # db.client = AsyncIOMotorClient(os.environ["MONGO_URI"])
    db.client = AsyncIOMotorClient(str("localhost:27017"),maxPoolSize=10,minPoolSize=10)

    db.vending = db.client.vending
    logging.info("Connected to DB.")

async def close_mongo_connection():
    logging.info("Closing MongoDB Connection...")
    db.client.close()
    logging.info("MongoDB Connection Closed.")