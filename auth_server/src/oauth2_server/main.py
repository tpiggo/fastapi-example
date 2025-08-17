from typing import Annotated, TypeVar

from fastapi import FastAPI, Header, Depends

from oauth2_server.models.user import BaseUser
from oauth2_server.service.user_service import (
    UserService,
    user_service as get_user_service,
)
from oauth2_server.service.token_service import (
    TokenService,
    token_service as get_token_service,
)

app = FastAPI(root_path="/api/v1")


@app.post("/authorize")
async def login(user: BaseUser, user_service: UserService = Depends(get_user_service)):
    return user_service.login(user)


@app.get("/token_info")
async def token_info(
    token: Annotated[str | None, Header()] = None,
    token_service: TokenService = Depends(get_token_service),
):
    return token_service.get_token_info(token)


@app.get("/user_info")
async def user_info(
    token: Annotated[str | None, Header()] = None,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user_info(token)
