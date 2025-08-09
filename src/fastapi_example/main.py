from typing import Union, Any

from fastapi import FastAPI, Depends

from fastapi_example.models.user import User
from fastapi_example.security import has_authorization

app = FastAPI()


@app.get("/")
def read_root():
    return User(username="hello")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None,
              user_info: dict[str, Any] = Depends(has_authorization(["api.scopes.v1"]))):
    return {"item_id": item_id, "q": q, "user_name": user_info['username']}
