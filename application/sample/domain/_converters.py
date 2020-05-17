import sample.domain.dto as _dto
import sample.repository.dto


class User:
    @classmethod
    def from_repository(
            cls, source: sample.repository.dto.User) -> _dto.User:
        return sample.domain.dto.User(id=source.id, email=source.email)
