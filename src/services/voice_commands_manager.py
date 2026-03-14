import subprocess
from logging import getLogger
from typing import Generator

from domain.interfaces import IVoiceCommands
from domain.models import VoiceCommand

logger = getLogger(__name__)


class VoiceCommandsManager:
    def __init__(self, voice_commands: IVoiceCommands):
        self._voice_commands = voice_commands

    def new_voice_command(
        self,
        name: str,
        description: str,
        exec: str,
        phrase: str,
        shell: bool,
    ) -> VoiceCommand:
        return self._voice_commands.create(
            name=name,
            description=description,
            exec=exec,
            shell=shell,
            phrase=phrase,
        )

    def get_voice_command_by_id(
        self,
        id: str,
    ) -> VoiceCommand | None:
        return self._voice_commands.get_by_id(id=id)

    def get_voice_command_by_phrase(
        self,
        phrase: str,
    ) -> VoiceCommand | None:
        return self._voice_commands.get_by_phrase(phrase=phrase)

    def update_voice_command(
        self,
        id: str,
        name: str,
        description: str,
        exec: str,
        phrase: str,
        shell: bool,
    ) -> bool:
        return self._voice_commands.update(
            id=id,
            name=name,
            description=description,
            exec=exec,
            phrase=phrase,
            shell=shell,
        )

    def delete_voice_command(
        self,
        id: str,
    ) -> bool:
        return self._voice_commands.delete(id=id)

    def get_voice_commands_list(self) -> list[VoiceCommand]:
        return self._voice_commands.get_all()

    def run_voice_command(self, instance: VoiceCommand):
        logger.debug(f"Running command: {instance}")
        subprocess.run(
            instance.exec,
            shell=instance.shell,
        )


__all__ = ("VoiceCommandsManager",)
