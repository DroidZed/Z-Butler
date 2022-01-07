# pylint: skip-file

from pymongo.collection import Collection
from pymongo.database import Database

from classes.mongo_db_connection import MongoDBConnection


class MongoDBHelperClient:

    """
    A helper classes used as a wrapper for all CRUD methods against the mongodb database.
    """

    def __init__(self, collection_name: str):
        self._mdb_connection: Database = MongoDBConnection().db_connection
        self._collection: Collection = self._mdb_connection[collection_name]

    def query_collection(self, payload: dict) -> list[dict] | None:

        """
        A CRUD method used to query a specific collection using the payload given in arguments.
        Args:
            payload: dict

        Returns:
                A list of documents fetched from the database. None if nothing is present.
        """

        return [c for c in self._collection.find(payload, {"_id": 0})]

    def insert_into_collection(self, payload: list[dict]) -> None:

        self._collection.insert_many(payload)

    def delete_from_collection(self, payload: dict) -> None:

        self._collection.delete_many(payload)

    def update_document(self, criteria: dict, payload: dict) -> None:

        self._collection.update_one(criteria, payload, upsert=True)
