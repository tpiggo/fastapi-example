from pydantic import BaseModel
from sqlmodel import SQLModel as Model, Field, Relationship


class BaseUser(BaseModel):
    username: str
    password: str

    def __hash__(self):
        return hash(self.username)


class Scope(Model, table=True):
    app_name: str = Field(primary_key=True)
    scope_name: str = Field(primary_key=True)
    suffix: str = Field(primary_key=True)
    id: int = Field()

    def as_string(self):
        return f"{self.app_name}.{self.scope_name}.v{self.suffix}"


class UserScopeLink(Model, table=True):
    __tablename__ = "user_scope_association"
    scope_id: int | None = Field(default=None, foreign_key="scope.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)


class User(BaseUser, Model, table=True):
    __tablename__ = "users"
    id: int = Field()
    username: str = Field(primary_key=True, max_length=255)
    password: str = Field(max_length=20)
    name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    scopes: list[Scope] = Relationship(link_model=UserScopeLink)
