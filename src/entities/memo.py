from dataclasses import dataclass
from datetime import datetime

@dataclass
class Memo:
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    project_path: str = ""  # プロジェクトパス
    command: str = ""  # 実行コマンド

    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row[0],
            user_id=row[1],
            title=row[2],
            content=row[3],
            created_at=datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'),
            project_path=row[5] if len(row) > 5 else "",
            command=row[6] if len(row) > 6 else ""
        ) 