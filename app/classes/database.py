import mysql.connector
from app.config.dbConfig import DBConfig


class DB:

    def __init__(self):
        mydb = mysql.connector.connect(
            host=DBConfig.host,
            user=DBConfig.user,
            password=DBConfig.password,
            database=DBConfig.database
        )

        print(mydb)
