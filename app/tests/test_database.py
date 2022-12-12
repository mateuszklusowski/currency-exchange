import os
from app.database import Database


def check_conn(connection):
    try:
        connection.cursor
        return True
    except Exception:
        return False


def test_sqlite_conenction():
    connection = Database("testdb.db")
    path = os.path.abspath("testdb.db")
    assert os.path.exists(path) == True
    assert check_conn(connection) == True
