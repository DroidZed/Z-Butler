from functions.mdb_connection import get_connection


class MongoDBConnection:
    _instance = None

    def __init__(self):
        self._db_connection = get_connection()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    @property
    def db_connection(self):
        return self._db_connection
