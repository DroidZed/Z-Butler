# pylint: skip-file

from classes.singleton_class import SingletonClass
from util.mdb_connection import get_connection


class MongoDBConnection(metaclass=SingletonClass):
    def __init__(self):
        self.__db_connection = get_connection()

    @property
    def db_connection(self):
        return self.__db_connection
