import time
from pydantic import BaseModel, Field
import random


class Token(BaseModel):
    username: str
    ttl: int = Field(default_factory=lambda: int(time.time() + 300))
