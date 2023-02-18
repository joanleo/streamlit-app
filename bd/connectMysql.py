import os
from mysql.connector import connect, Error
from dotenv import load_dotenv


def conexionDb():
    load_dotenv()
    try:
        connection = connect(
            host = os.getenv('HOST'),
            user = os.getenv('USER'),
            passwd = os.getenv('PASSWD'),
            db = os.getenv('DB'),
            port = os.getenv('PORT')
        )
        return connection
    except Error as error:
        print(error)
