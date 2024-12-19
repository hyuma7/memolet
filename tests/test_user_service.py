import unittest
import os
import sqlite3
import bcrypt
from src.services.user_service import UserService
from src.database.connection import DatabaseConnection

class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # テスト用のデータベースファイル名
        cls.test_db = "test_memos.db"
        
        # データベース接続をモック
        def get_test_connection():
            if not hasattr(DatabaseConnection._thread_local, "connection"):
                DatabaseConnection._thread_local.connection = sqlite3.connect(cls.test_db)
            return DatabaseConnection._thread_local.connection
        
        DatabaseConnection.get_connection = staticmethod(get_test_connection)

    def setUp(self):
        # テストデータベースの初期化
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        # usersテーブルの作成
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        
        # テストデータのクリーンアップ
        cursor.execute("DELETE FROM users")
        conn.commit()

    def tearDown(self):
        # テストデータのクリーンアップ
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()

    @classmethod
    def tearDownClass(cls):
        # テストデータベースの削除
        DatabaseConnection.close_connection()
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    def test_register_user_success(self):
        service = UserService()
        result = service.register_user("testuser", "password123")
        self.assertTrue(result)
        
        # データベースに正しく保存されているか確認
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users WHERE username = ?", ("testuser",))
        row = cursor.fetchone()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "testuser")
        self.assertTrue(bcrypt.checkpw("password123".encode(), row[1]))

    def test_register_duplicate_user(self):
        service = UserService()
        # 1回目の登���
        service.register_user("testuser", "password123")
        # 2回目の登録（重複）
        result = service.register_user("testuser", "password456")
        self.assertFalse(result)

    def test_authenticate_user_success(self):
        service = UserService()
        # ユーザーを登録
        service.register_user("testuser", "password123")
        
        # 認証テスト
        user = service.authenticate_user("testuser", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_authenticate_user_wrong_password(self):
        service = UserService()
        # ユーザーを登録
        service.register_user("testuser", "password123")
        
        # 誤ったパスワードで認証テスト
        user = service.authenticate_user("testuser", "wrongpassword")
        self.assertIsNone(user)

    def test_authenticate_nonexistent_user(self):
        service = UserService()
        user = service.authenticate_user("nonexistent", "password123")
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main() 