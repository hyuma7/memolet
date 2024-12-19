import sqlite3
from threading import local

class DatabaseConnection:
    _thread_local = local()

    @classmethod
    def get_connection(cls):
        if not hasattr(cls._thread_local, "connection"):
            cls._thread_local.connection = sqlite3.connect("memos.db")
        return cls._thread_local.connection

    @classmethod
    def close_connection(cls):
        if hasattr(cls._thread_local, "connection"):
            cls._thread_local.connection.close()
            del cls._thread_local.connection