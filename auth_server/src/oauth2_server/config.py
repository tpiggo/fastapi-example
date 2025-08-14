from typing import Literal

from pydantic import BaseModel
import config_loader as cl


class TokenProducerConfiguration(BaseModel):
    secret: str
    algorithm: Literal["HS256", "SHA256"]


class Properties(BaseModel):
    tokens: TokenProducerConfiguration
    app_name: str


configuration = cl.configuration_properties(Properties)
