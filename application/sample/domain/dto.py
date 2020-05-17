import dataclasses


@dataclasses.dataclass(frozen=True)
class DraftUser:
    email: str
    password: str


@dataclasses.dataclass(frozen=True)
class SignIn:
    email: str
    password: str


@dataclasses.dataclass(frozen=True)
class User:
    id: int
    email: str
