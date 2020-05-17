from __future__ import annotations
from typing import (
    Iterable,
    Iterator,
    Tuple,
    TypeVar,
)

import sample.repository._definitions
import sample.repository._definitions as _definitions
import sample.repository.dto
import sample.repository.dto as _dto


_T = TypeVar('_T')


def sequence(items: Iterable[_T]) -> Iterator[Tuple[int, _T]]:
    return ((i, item) for i, item in enumerate(items, start=1))


class Migration:
    @classmethod
    def to_entity(
            cls, source: sample.repository._definitions.Migration
    ) -> sample.repository.dto.Migration:
        return sample.repository.dto.Migration(
            version=source.version, applied_at=source.applied_at)


class User:
    @classmethod
    def to_dto(cls, source: _definitions.User) -> _dto.User:
        return _dto.User(
            id=source.id, email=source.email, password=source.password)
