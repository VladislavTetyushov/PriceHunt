import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
data_filename = os.getenv("DATABASE_PATH")
assert data_filename is not None


def execute_query(query):
    with sqlite3.connect(data_filename) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()


def execute_read_query(query):
    with sqlite3.connect(data_filename) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
