import os

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from pydantic import SecretStr

from openhands.server.settings import Settings
from openhands.storage.data_models.user_secrets import UserSecrets
from openhands.storage.secrets.secrets_store import SecretsStore
from openhands.storage.settings.settings_store import SettingsStore

_SESSION_API_KEY = os.getenv('SESSION_API_KEY')
_SESSION_API_KEY_HEADER = APIKeyHeader(name='X-Session-API-Key', auto_error=False)


def check_session_api_key(
    session_api_key: str | None = Depends(_SESSION_API_KEY_HEADER),
):
    """Check the session API key and throw an exception if incorrect. Having this as a dependency
    means it appears in OpenAPI Docs
    """
    if session_api_key != _SESSION_API_KEY:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)


def get_dependencies() -> list[Depends]:
    result = []
    if _SESSION_API_KEY:
        result.append(Depends(check_session_api_key))
    return result


async def get_provider_tokens(request: Request):
    return None


async def get_access_token(request: Request) -> SecretStr | None:
    return None


async def get_user_id(request: Request) -> str | None:
    return None


async def get_user_email(request: Request) -> str | None:
    return None


async def get_user_settings_store(request: Request) -> SettingsStore:
    from openhands.storage.settings.local_settings_store import LocalSettingsStore
    return LocalSettingsStore()


async def get_user_settings(request: Request) -> Settings | None:
    settings_store = await get_user_settings_store(request)
    return await settings_store.load()


async def get_secrets_store(request: Request) -> SecretsStore:
    from openhands.storage.secrets.local_secrets_store import LocalSecretsStore
    return LocalSecretsStore()


async def get_user_secrets(request: Request) -> UserSecrets | None:
    secrets_store = await get_secrets_store(request)
    return await secrets_store.load()


async def get_auth_type(request: Request):
    return None
