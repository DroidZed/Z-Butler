from typing import Any, Optional
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from pymongo.results import (
    InsertManyResult,
    DeleteResult,
    UpdateResult,
)

from utils.singleton_class import SingletonClass
from utils import Env


class MongoDBConnection(metaclass=SingletonClass):
    def __init__(self) -> None:
        self.__db_connection: AsyncIOMotorClient = AsyncIOMotorClient(
            Env.MDB_SRV, serverSelectionTimeoutMS=5000
        )

    @property
    def db_connection(self) -> AsyncIOMotorDatabase:
        return self.__db_connection[Env.DB_NAME]

    def close_connection(self) -> None:
        self.__db_connection.close()


class MongoDBHelperClient:
    """
    A helper classes used as a wrapper for all CRUD methods against the mongodb database.
    """

    def __init__(self, collection_name: str):
        self._mdb_connection: AsyncIOMotorDatabase = MongoDBConnection().db_connection
        self._collection: AsyncIOMotorCollection = self._mdb_connection[collection_name]

    async def query_collection(self, payload: dict[str, Any]) -> list[dict] | None:
        """
        A CRUD method used to query a specific collection using the payload given in arguments.
        Args:
            payload: dict

        Returns:
                A list of documents fetched from the database. None if nothing is present.
        """

        return [c async for c in self._collection.find(payload, {"_id": 0, "__v": 0})]

    async def query_document(self, payload: dict[str, Any]) -> Optional[dict[str, Any]]:
        """
        A CRUD method used to query a specific document from a collection using the payload given in arguments.
        Args:
            payload: dict

        Returns:
                A list of documents fetched from the database. None if nothing is present.
        """

        val: Optional[dict[str, Any]] = await self._collection.findOne(
            payload, {"_id": 0, "__v": 0}
        )

        return val

    async def insert_into_collection(self, payload: list[dict]) -> InsertManyResult:
        return await self._collection.insert_many(payload)

    async def delete_from_collection(self, payload: dict) -> DeleteResult:
        return await self._collection.delete_many(payload)

    async def update_document(
        self,
        criteria: dict,
        payload: dict,
        upsert: bool = True,
    ) -> UpdateResult:
        return await self._collection.update_one(criteria, payload, upsert=upsert)
