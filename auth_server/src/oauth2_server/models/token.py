import time
from pydantic import BaseModel, Field
import random


class Token(BaseModel):
    username: str
    fun_int: int = Field(default_factory=lambda: random.randint(1, 100000))
    ttl: int = Field(default_factory=lambda: int(time.time() + 300))
