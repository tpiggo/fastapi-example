from typing import Union

from fastapi import FastAPI

from fastapi_example.models.user import User

app = FastAPI()


@app.get("/")
def read_root():
    return User(username="hello")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
