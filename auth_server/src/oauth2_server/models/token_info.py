from pydantic import BaseModel


class TokenInfo(BaseModel):
    token: str
    ttl: int
    refresh_token: str
