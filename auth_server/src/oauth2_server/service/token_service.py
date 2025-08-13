import time
from fastapi import HTTPException, status
import jwt

from oauth2_server.models.token import Token
from oauth2_server.models.token_info import TokenInfo


class TokenService:
    secrets = "something_fun"
    algo = "HS256"

    def __init__(self):
        self.tokens: set[str] = set()

    def generate_token(self, username: str):
        token = jwt.encode(
            Token(username=username).model_dump(),
            self.secrets,
            algorithm=self.algo,
        )
        self.tokens.add(token)
        return token

    def validate_token(self, token: str) -> Token:
        time_now = time.time()
        try:
            token_decoded = Token(
                **jwt.decode(token, self.secrets, algorithms=[self.algo])
            )
            if token_decoded.ttl >= time_now:
                return token_decoded
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Expired or invalid token"
            )
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or incorrect token",
            )

    def get_token_info(self, token: str):
        token_obj = self.validate_token(token)

        return TokenInfo(
            token=token, ttl=int(token_obj.ttl - time.time()), refresh_token=""
        )


def token_service() -> TokenService:
    return TokenService()
