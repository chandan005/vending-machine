from motor.motor_asyncio import AsyncIOMotorClient

class DataBase:
    client: AsyncIOMotorClient = None
    vending = None

db = DataBase()