from oauth2_server.models.user import ValidUser, User
from oauth2_server.models.user_info import UserInfo
from oauth2_server.service.token_service import (
    TokenService,
    token_service as get_token_service,
)
from fastapi import Depends, HTTPException, status


class UserService:
    def __init__(self, token_service: TokenService):
        self.users = {
            u.username: u
            for u in [
                ValidUser(username="timmy", password="tt", scopes=["api.scopes.v1"])
            ]
        }
        self.token_service = token_service

    def get_user_info(self, token: str):
        user = self.users[self.token_service.validate_token(token).username]
        return UserInfo(username=user.username, scopes=user.scopes)

    def login(self, user: User):
        if (
            user.username not in self.users
            or self.users[user.username].password != user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return self.token_service.generate_token(user.username)


def user_service(token_service: TokenService = Depends(get_token_service)):
    return UserService(token_service)
