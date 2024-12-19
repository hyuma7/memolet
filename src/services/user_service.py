import bcrypt
from ..database.connection import DatabaseConnection
from ..entities.user import User

class UserService:
    def authenticate_user(self, username: str, password: str) -> User | None:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        
        if row and bcrypt.checkpw(password.encode(), row[2]):
            return User(row[0], row[1], row[2])
        return None

    def register_user(self, username: str, password: str) -> bool:
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            
            # ユーザー名の重複チェック
            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return False
            
            # パスワードのハッシュ化
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed)
            )
            conn.commit()
            return True
        except Exception:
            return False 