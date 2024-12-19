from datetime import datetime
from typing import List, Dict
from ..database.connection import DatabaseConnection
from ..entities.memo import Memo, Command

class MemoService:
    def create_memo(self, user_id: int, title: str, content: str, project_path: str = "", commands: List[Dict] = None) -> bool:
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # メモの作成
            cursor.execute(
                "INSERT INTO memos (user_id, title, content, created_at, project_path) VALUES (?, ?, ?, ?, ?)",
                (user_id, title, content, created_at, project_path)
            )
            memo_id = cursor.lastrowid
            
            # コマンドの作成
            if commands:
                for i, cmd in enumerate(commands):
                    cursor.execute(
                        "INSERT INTO commands (memo_id, name, command, order_index) VALUES (?, ?, ?, ?)",
                        (memo_id, cmd['name'], cmd['command'], i)
                    )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating memo: {e}")
            return False

    def get_user_memos(self, user_id: int) -> list[Memo]:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        # メモの取得
        cursor.execute(
            "SELECT id, user_id, title, content, created_at, project_path FROM memos WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        memos = [Memo.from_db_row(row) for row in cursor.fetchall()]
        
        # 各メモのコマンドを取得
        for memo in memos:
            cursor.execute(
                "SELECT id, name, command, order_index FROM commands WHERE memo_id = ? ORDER BY order_index",
                (memo.id,)
            )
            memo.commands = [Command(id=row[0], name=row[1], command=row[2], order_index=row[3]) 
                           for row in cursor.fetchall()]
        
        return memos

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
        
        # メモの取得
        cursor.execute(
            "SELECT id, user_id, title, content, created_at, project_path FROM memos WHERE id = ? AND user_id = ?",
            (memo_id, user_id)
        )
        row = cursor.fetchone()
        if not row:
            return None
            
        memo = Memo.from_db_row(row)
        
        # コマンドの取得
        cursor.execute(
            "SELECT id, name, command, order_index FROM commands WHERE memo_id = ? ORDER BY order_index",
            (memo_id,)
        )
        memo.commands = [Command(id=row[0], name=row[1], command=row[2], order_index=row[3]) 
                        for row in cursor.fetchall()]
        
        return memo

    def update_memo(self, memo_id: int, user_id: int, title: str, content: str, 
                   project_path: str = "", commands: List[Dict] = None) -> bool:
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            
            # メモの更新
            cursor.execute(
                "UPDATE memos SET title = ?, content = ?, project_path = ? WHERE id = ? AND user_id = ?",
                (title, content, project_path, memo_id, user_id)
            )
            
            # 既存のコマンドを削除
            cursor.execute("DELETE FROM commands WHERE memo_id = ?", (memo_id,))
            
            # 新しいコマンドを追加
            if commands:
                for i, cmd in enumerate(commands):
                    cursor.execute(
                        "INSERT INTO commands (memo_id, name, command, order_index) VALUES (?, ?, ?, ?)",
                        (memo_id, cmd['name'], cmd['command'], i)
                    )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating memo: {e}")
            return False 