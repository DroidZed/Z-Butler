from classes.singleton_class import SingletonClass
from util.mdb_connection import async_db_connection


class MongoDBConnection(metaclass=SingletonClass):
    def __init__(self):
        self.__db_connection = async_db_connection()

    @property
    def db_connection(self):
        return self.__db_connection
