from typing import Annotated, TypeVar

from fastapi import FastAPI, Header, Depends

from oauth2_server.models.user import User
from oauth2_server.service.user_service import (
    UserService,
    user_service as get_user_service,
)
from oauth2_server.service.token_service import (
    TokenService,
    token_service as get_token_service,
)

app = FastAPI()

secrets = "secret"
algo = "HS256"

T = TypeVar("T")


@app.post("/api/v1/authorize")
async def login(user: User, user_service: UserService = Depends(get_user_service)):
    return user_service.login(user)


@app.post("/api/v1/token_info")
async def token_info(
    token: Annotated[str | None, Header()] = None,
    token_service: TokenService = Depends(get_token_service),
):
    return token_service.get_token_info(token)


@app.post("/api/v1/user_info")
async def user_info(
    token: Annotated[str | None, Header()] = None,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user_info(token)
