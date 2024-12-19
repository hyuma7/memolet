import sqlite3

def init_database():
    conn = sqlite3.connect("memos.db")
    cursor = conn.cursor()

    # usersテーブルの作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # memosテーブルの作成（commandカラムを削除）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS memos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        project_path TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # commandsテーブルの作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        memo_id INTEGER NOT NULL,
        command TEXT NOT NULL,
        name TEXT NOT NULL,
        order_index INTEGER NOT NULL,
        FOREIGN KEY (memo_id) REFERENCES memos (id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("データベースの初期化が完了しました。") 