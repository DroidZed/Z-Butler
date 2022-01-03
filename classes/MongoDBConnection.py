from classes.SingletonClass import SingletonClass
from functions.mdb_connection import get_connection


class MongoDBConnection(metaclass=SingletonClass):

    def __init__(self):
        self._db_connection = get_connection()

    @property
    def db_connection(self):
        return self._db_connection
