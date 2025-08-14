from typing import Callable, Annotated, Coroutine, Any

from fastapi import Depends, Header, HTTPException, status
import aiohttp


class SecurityService:
    _url = "http://localhost:8081/api/v1"

    def __init__(self):
        self.http_client = aiohttp.ClientSession()

    @classmethod
    def _json_throw_error(cls, res: aiohttp.ClientResponse):
        res.raise_for_status()
        return res

    async def _generic_get(self, url_part: str, token: str):
        async with aiohttp.ClientSession() as client:
            async with client.get(f"{self._url}/{url_part}", headers={"token": token}) as resp:
                return await self._json_throw_error(resp).json()

    async def token_info(self, token: str):
        return await self._generic_get("token_info", token)

    async def get_user_info(self, token: str) -> dict[str, Any]:
        return await self._generic_get("user_info", token)


# Singleton service shared with external elements
_service = SecurityService()


def _security_handler() -> SecurityService:
    return _service


def has_authorization(scopes: list[str]) -> Callable[[str], Coroutine[Any, Any, dict[str, Any]]]:
    """
    Function to handle calling the endpoint with the proper rights.
    Uses closures to handle the rights management
    :param scopes: required scopes
    :return: User info
    """
    set_of_scopes = set(scopes)

    async def check_rights(token: Annotated[str | None, Header()] = None,
                           security_service: SecurityService = Depends(_security_handler)):
        user_info = await security_service.get_user_info(token)
        if set_of_scopes.difference(user_info['scopes']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid permissions to view this resource"
            )
        return user_info

    return check_rights
