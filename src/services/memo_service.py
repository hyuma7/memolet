from datetime import datetime
from ..database.connection import DatabaseConnection
from ..entities.memo import Memo

class MemoService:
    def create_memo(self, user_id: int, title: str, content: str, project_path: str = "", command: str = "") -> bool:
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO memos (user_id, title, content, created_at, project_path, command) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, title, content, created_at, project_path, command)
            )
            conn.commit()
            return True
        except Exception:
            return False

    def get_user_memos(self, user_id: int) -> list[Memo]:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, user_id, title, content, created_at, project_path, command FROM memos WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        return [Memo.from_db_row(row) for row in cursor.fetchall()]

    def delete_memo(self, memo_id: int, user_id: int) -> bool:
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memos WHERE id = ? AND user_id = ?", (memo_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            return False

    def get_memo(self, memo_id: int, user_id: int) -> Memo | None:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, user_id, title, content, created_at, project_path, command FROM memos WHERE id = ? AND user_id = ?",
            (memo_id, user_id)
        )
        row = cursor.fetchone()
        return Memo.from_db_row(row) if row else None 