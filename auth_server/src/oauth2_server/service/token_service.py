import time
from fastapi import HTTPException, status, Depends
import jwt

from oauth2_server.config import Properties, configuration, TokenProducerConfiguration
from oauth2_server.models.token import Token
from oauth2_server.models.token_info import TokenInfo


class TokenService:
    config: TokenProducerConfiguration

    def __init__(self, props: Properties):
        self.config = props.tokens

    def generate_token(self, username: str):
        token = jwt.encode(
            Token(username=username).model_dump(),
            self.config.secret,
            algorithm=self.config.algorithm,
        )
        return token

    def validate_token(self, token: str) -> Token:
        time_now = time.time()
        try:
            token_decoded = Token(
                **jwt.decode(token, self.config.secret, algorithms=[self.config.algorithm])
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


def token_service(props: Properties = Depends(configuration)) -> TokenService:
    return TokenService(props)
