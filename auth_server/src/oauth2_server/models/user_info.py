from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    username: str
    scopes: list[str]
    email: str
