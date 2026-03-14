from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceCommand:
    id: str
    name: str
    description: str
    exec: str
    phrase: str
    shell: bool


__all__ = ("VoiceCommand",)
