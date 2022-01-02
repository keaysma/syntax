import psycopg2
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DatabaseConnection():

    def __prepare_database(self):
        database_exists = False
        with self.__prio__conn.cursor() as c:
            c.execute(f"SELECT datname FROM pg_catalog.pg_database WHERE datname='{self.database}';")
            database_exists = bool(len(c.fetchall()))

        if database_exists == True:
            return

        with self.__prio__conn.cursor() as c:
            c.execute(f"CREATE DATABASE {self.database}")

        

    def __init__(self, host='localhost', database='syntax_words', user='postgres', password='postgres'):

        self.host = host
        self.database = database
        self.user = user
        # We are not keeping the password

        # Ensure the existance of the database
        self.__prio__conn : psycopg2.extensions.connection = connect(
            host = self.host, 
            database = 'postgres', 
            user = self.user, 
            password = password
        )

        self.__prio__conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        self.__prepare_database()

        # Keep the database connection
        self.__conn : psycopg2.extensions.connection = connect(
            host = self.host, 
            database = self.database, 
            user = self.user, 
            password = password
        )

        return

    def __del__(self):
        if self.__conn != None:
            self.__conn.close()

        if self.__prio__conn != None:
            self.__prio__conn.close()

def create_database(host='localhost', database='syntax_words', user='postgres', password='postgres'):
    temp_conn = DatabaseConnection(
        host = host,
        database = database,
        user = user,
        password = password
    )
    del temp_conn