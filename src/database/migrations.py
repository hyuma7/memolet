from .connection import DatabaseConnection

class DatabaseMigrations:
    @staticmethod
    def run_migrations():
        conn = DatabaseConnection().connection
        cursor = conn.cursor()

        # ユーザーテーブルの作成
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
        ''')

        # メモテーブルの作成
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            created_at TEXT,
            project_path TEXT,
            command TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        conn.commit() 