from sqlmodel import Session, select

from oauth2_server.models.user import User, BaseUser
from oauth2_server.models.user_info import UserInfo
from oauth2_server.service.db_service import SessionDep
from oauth2_server.service.token_service import (
    TokenService,
    token_service as get_token_service,
)
from fastapi import Depends, HTTPException, status


class UserService:
    def __init__(self, token_service: TokenService, db_session: Session):
        self.token_service = token_service
        self.db_session = db_session

    def get_user_info(self, token: str):
        user = self.db_session.exec(
            select(User).filter_by(
                username=self.token_service.validate_token(token).username
            )
        ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find the user"
            )
        return UserInfo(
            username=user.username,
            scopes=[scope.as_string() for scope in user.scopes],
            id=user.id,
            email=user.email,
        )

    def login(self, user: BaseUser):
        found_user = self.db_session.exec(
            select(User).filter_by(username=user.username)
        ).first()
        if not found_user or found_user.password != user.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return self.token_service.generate_token(user.username)


def user_service(
    session: SessionDep, token_service: TokenService = Depends(get_token_service)
):
    return UserService(token_service, session)
