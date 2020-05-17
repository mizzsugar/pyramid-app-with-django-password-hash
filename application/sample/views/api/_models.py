import pydantic


class SignIn(pydantic.BaseModel):
    email: str
    password: str


class SignUp(pydantic.BaseModel):
    email: str
    password: str
