from pymongo.collection import Collection
from pymongo.database import Database

from classes.MongoDBConnection import MongoDBConnection


class MongoDBHelperClient:

    def __init__(self, collection_name: str):
        self._mdb_connection: Database = MongoDBConnection().db_connection
        self._collection: Collection = self._mdb_connection[collection_name]

    def query_all_from_collection(self) -> list[dict]:

        return [c for c in self._collection.find({}, {"_id": 0})]

    def query_collection(self, payload: dict) -> list[dict] | None:

        return [c for c in self._collection.find(payload, {"_id": 0})]

    def insert_into_collection(self, payload: list[dict]) -> None:

        self._collection.insert_many(payload)

    def delete_from_collection(self,  payload: dict) -> None:

        self._collection.delete_many(payload)

    def update_document(self, criteria: dict, payload: dict) -> None:

        self._collection.update_one(criteria, payload, upsert=True)
