from pymongo.collection import Collection
from pymongo.database import Database

from classes.MongoDBConnection import MongoDBConnection


class MongoDBHelperClient:

    def __init__(self):
        self._mdb_connection: Database = MongoDBConnection().db_connection

    def query_all_from_collection(self, collection_name: str) -> list[dict]:

        if not collection_name:
            return

        collection: Collection = self._mdb_connection[collection_name]

        return [c for c in collection.find({}, {"_id": 0})]

    def query_collection(self, collection_name: str, payload: dict) -> list[dict] | None:

        if not collection_name or not payload:
            return

        collection: Collection = self._mdb_connection[collection_name]

        return [c for c in collection.find(payload, {"_id": 0})]

    def insert_into_collection(self, collection_name: str, payload: list[dict]) -> None:

        if not collection_name or not payload:
            return

        collection: Collection = self._mdb_connection[collection_name]

        collection.insert_many(payload)

    def delete_from_collection(self, collection_name: str, payload: dict) -> None:

        if not collection_name:
            return

        collection: Collection = self._mdb_connection[collection_name]

        collection.delete_many(payload)

    def update_document(self, collection_name: str, criteria: dict, payload: dict) -> None:

        if not collection_name:
            return

        collection: Collection = self._mdb_connection[collection_name]

        collection.update_one(criteria, payload, upsert=True)
