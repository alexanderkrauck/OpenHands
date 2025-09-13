from types import MappingProxyType
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from openhands.events.stream import EventStream


class CustomSecret:
    def __init__(self, secret: str, description: str = ''):
        self.secret = secret
        self.description = description


class UserSecrets(BaseModel):
    provider_tokens: dict = Field(default_factory=dict)
    custom_secrets: dict[str, CustomSecret] = Field(default_factory=dict)

    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    def set_event_stream_secrets(self, event_stream: EventStream) -> None:
        """Set custom secrets in event stream for runtime access"""
        for secret_name, secret_obj in self.custom_secrets.items():
            if hasattr(secret_obj, 'secret'):
                event_stream.add_event_stream_secret(secret_name, secret_obj.secret)