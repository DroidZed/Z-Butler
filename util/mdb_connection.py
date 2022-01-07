from pymongo import MongoClient
from pymongo.database import Database

from config.main import DB_NAME, MDB_SRV


def get_connection() -> Database:

    """
    A function useful for getting a connection to a mongo database.

    Returns:
        A Database instance connected to the SRV string loaded from the env.

    """

    client = MongoClient(MDB_SRV)

    return client[DB_NAME]
