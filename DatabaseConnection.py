import mysql.connector

class DatabaseConnection:
    _instance = None

    host = 'localhost'
    user = 'root'
    password = ''
    database = 'gasfinder'

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = mysql.connector.connect(
                host=cls.host,
                user=cls.user,
                password=cls.password,
                database=cls.database
            )
        return cls._instance

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result