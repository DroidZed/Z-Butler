from pymongo import MongoClient
from pymongo.database import Database

from config.main import DB_NAME, MDB_SRV


def get_connection() -> Database:

    client = MongoClient(MDB_SRV)

    return client[DB_NAME]
