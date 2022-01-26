from motor.motor_asyncio import AsyncIOMotorClient

from config.main import DB_NAME, MDB_SRV


def async_db_connection():

    client = AsyncIOMotorClient(MDB_SRV, serverSelectionTimeoutMS=5000)

    return client[DB_NAME]
