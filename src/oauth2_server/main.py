import random
from typing import Annotated

from fastapi import FastAPI, status, HTTPException, Header

import jwt

from oauth2_server.models.user import ValidUser, User
from oauth2_server.models.user_info import UserInfo

app = FastAPI()

USERS: dict[str, ValidUser] = {
    u.username: u
    for u in [ValidUser(username="timmy", password="tt", scopes=["api.scopes.v1"])]
}

secrets = "secret"
algo = "HS256"


@app.post("/api/v1/login")
def login(user: User):
    if user.username not in USERS or USERS[user.username].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"token": jwt.encode(
        {"user": user.username, "rand_int": str(random.randint(1, 100))},
        secrets,
        algorithm=algo,
    )}


@app.post("/api/v1/authorize")
def authorize(token: Annotated[str | None, Header()] = None):
    token_decoded = jwt.decode(token, secrets, algorithms=[algo])
    if token_decoded['user'] in USERS:
        return UserInfo(
            username=USERS[token_decoded['user']].username,
            scopes=USERS[token_decoded['user']].scopes
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or incorrect token",
        headers={"WWW-Authenticate": "Basic"},
    )