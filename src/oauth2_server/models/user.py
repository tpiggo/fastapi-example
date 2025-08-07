from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

    def __hash__(self):
        return hash(self.username)


class ValidUser(User):
    scopes: list[str]
