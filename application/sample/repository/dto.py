from __future__ import annotations

import dataclasses
import datetime


@dataclasses.dataclass(frozen=True)
class Migration:
    version: int
    applied_at: datetime.datetime


@dataclasses.dataclass(frozen=True)
class User:
    id: int
    email: str
    password: str


@dataclasses.dataclass(frozen=True)
class DraftUser:
    email: str
    password: str
