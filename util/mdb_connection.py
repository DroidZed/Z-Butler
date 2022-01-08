from motor.motor_asyncio import AsyncIOMotorClient

from config.main import DB_NAME, MDB_SRV


# TODO: rewrite your mdb helper client and mongodb connection to use this function


def async_db_connection():

    """
    A function that establishes a connection through Motor to a mongodb database.

    Returns:
        A connected async client to a mongodb database.

    """

    client = AsyncIOMotorClient(MDB_SRV, serverSelectionTimeoutMS=5000)

    return client[DB_NAME]
