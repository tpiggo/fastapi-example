from typing import Callable, Annotated, Coroutine, Any

from fastapi import Depends, Header, HTTPException, status
import httpx


class SecurityService:
    _url = "http://localhost:8080/api/v1"

    @classmethod
    def _json_throw_error(cls, res: httpx.Response):
        res.raise_for_status()
        return res.json()

    async def token_info(self, token: str):
        async with httpx.AsyncClient() as client:
            return self._json_throw_error(await client.get(f"{self._url}/token_info", headers={"token": token}))

    async def get_user_info(self, token: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            return self._json_throw_error(await client.get(f"{self._url}/user_info", headers={"token": token}))


def _security_handler() -> SecurityService:
    return SecurityService()


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
