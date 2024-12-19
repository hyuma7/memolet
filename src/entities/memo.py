from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Command:
    id: int
    name: str
    command: str
    order_index: int

@dataclass
class Memo:
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    project_path: str
    commands: List[Command]

    @staticmethod
    def from_db_row(row) -> 'Memo':
        if not row:
            return None
        return Memo(
            id=row[0],
            user_id=row[1],
            title=row[2],
            content=row[3],
            created_at=datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'),
            project_path=row[5],
            commands=[]  # コマンドは別途取得
        ) 