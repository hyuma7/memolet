from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    password: str  # ハッシュ化されたパスワード

    def __init__(self, id: int, username: str, password: str = None):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(row[0], row[1], row[2] if len(row) > 2 else None) 