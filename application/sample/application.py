import dataclasses
import os
from typing import (
    TypedDict,
)


@dataclasses.dataclass(frozen=True)
class SQLite3ettings:
    db_name: str

    def as_dsn(self) -> str:
        return f'sqlite:///{self.db_name}'


class Settings(TypedDict):
    sqlite3: SQLite3ettings


def settings() -> Settings:
    return {
        'sqlite3': SQLite3ettings(
            db_name=os.getenv('DATABASE_NAME', 'db.sqlite3')
        ),
    }
