from pydantic import BaseModel


class UserInfo(BaseModel):
    username: str
    scopes: list[str]