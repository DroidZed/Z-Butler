from motor.motor_asyncio import AsyncIOMotorClient

from utils.singleton_class import SingletonClass
from utils import Env


class MongoDBConnection(metaclass=SingletonClass):
    def __init__(self):
        self.__db_connection = AsyncIOMotorClient(
            Env.MDB_SRV, serverSelectionTimeoutMS=5000
        )[Env.DB_NAME]

    @property
    def db_connection(self):
        return self.__db_connection


class MongoDBHelperClient:
    """
    A helper classes used as a wrapper for all CRUD methods against the mongodb database.
    """

    def __init__(self, collection_name: str):
        self._mdb_connection = MongoDBConnection().db_connection
        self._collection = self._mdb_connection[collection_name]

    async def query_collection(self, payload: dict) -> list[dict] | None:
        """
        A CRUD method used to query a specific collection using the payload given in arguments.
        Args:
            payload: dict

        Returns:
                A list of documents fetched from the database. None if nothing is present.
        """

        return [
            c
            async for c in self._collection.find(payload, {"_id": 0, "__v": 0})
        ]

    async def insert_into_collection(self, payload: list[dict]) -> None:
        await self._collection.insert_many(payload)

    async def delete_from_collection(self, payload: dict) -> None:
        await self._collection.delete_many(payload)

    async def update_document(
        self,
        criteria: dict,
        payload: dict,
        upsert: bool = True,
    ) -> None:
        await self._collection.update_one(criteria, payload, upsert=upsert)
