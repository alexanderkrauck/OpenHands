from __future__ import annotations

from pydantic import (
    BaseModel,
    ConfigDict,
    SecretStr,
)

from openhands.core.config.mcp_config import MCPConfig
from openhands.storage.data_models.settings import Settings


class POSTProviderModel(BaseModel):
    """Settings for POST requests"""

    mcp_config: MCPConfig | None = None


class POSTCustomSecrets(BaseModel):
    """Adding new custom secret"""

    pass


class GETSettingsModel(Settings):
    """Settings with additional token data for the frontend"""

    pass
    llm_api_key_set: bool
    search_api_key_set: bool = False

    model_config = ConfigDict(use_enum_values=True)


