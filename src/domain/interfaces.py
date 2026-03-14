from typing import Generator
from abc import ABC

from domain.models import VoiceCommand


class IVoiceCommands(ABC):
    def get_by_id(self, id: str) -> VoiceCommand | None: ...
    def get_by_phrase(self, phrase: str) -> VoiceCommand | None: ...
    def create(
        self,
        name: str,
        description: str,
        exec: str,
        phrase: str,
        shell: bool,
    ) -> VoiceCommand: ...
    def delete(self, id: str) -> bool: ...
    def update(
        self,
        id: str,
        name: str | None = None,
        description: str | None = None,
        exec: str | None = None,
        phrase: str | None = None,
        shell: bool | None = None,
    ) -> bool: ...
    def get_all(self) -> list[VoiceCommand]: ...


__all__ = ("IVoiceCommands",)
