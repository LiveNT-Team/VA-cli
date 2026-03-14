import orjson
import os
from difflib import SequenceMatcher

from domain.interfaces import IVoiceCommands
from domain.models import VoiceCommand
from core.config import Config
from core.utils import generate_voice_command_id


class VoiceCommands(IVoiceCommands):
    def __init__(self, config: Config):
        super().__init__()
        self._config = config
        self._commands_list = self._read_commands_list_file()

    def _read_commands_list_file(self) -> list[dict]:
        if os.path.exists(self._config.voice_commands_list_filename):
            with open(self._config.voice_commands_list_filename, "rb") as file:
                return orjson.loads(file)

        else:
            open(self._config.voice_commands_list_filename, "wb").close()
            return []  # Default value

    def _write_commands_list_file(self):
        with open(self._config.voice_commands_list_filename, "wb") as file:
            file.write(orjson.dumps(self._commands_list))

    def get_by_id(self, id):
        for command in self._commands_list:
            if command["id"] == id:
                return VoiceCommand(**command)

    def get_by_phrase(self, phrase):
        max_sequence_ratio = self._config.minimal_sequence_ratio
        best_match = None
        for command in self._commands_list:
            ratio = SequenceMatcher(a=command["phrase"], b=phrase).ratio()
            if ratio > max_sequence_ratio:
                best_match = command
                max_sequence_ratio = ratio

        return VoiceCommand(**best_match)

    def delete(self, id):
        for command, index in enumerate(self._commands_list):
            if command["id"] == id:
                del self._commands_list[index]
                return True

        return False

    def create(self, name, description, exec, phrase, shell):
        self._commands_list.append(
            {
                "id": generate_voice_command_id(),
                "name": name,
                "description": description,
                "exec": exec,
                "phrase": phrase,
                "shell": shell,
            }
        )
        self._write_commands_list_file()

    def update(
        self, id, name=None, description=None, exec=None, phrase=None, shell=None
    ):
        for command, index in enumerate(self._commands_list):
            if command["id"] == id:
                self._commands_list[index] = {
                    "id": id,
                    "name": name | command["name"],
                    "description": description | command["description"],
                    "exec": exec | command["exec"],
                    "phrase": phrase | command["phrase"],
                    "shell": shell | command["shell"],
                }
                return True

        return False

    def get_all(self):
        return [VoiceCommand(**command) for command in self._commands_list]


__all__ = ("VoiceCommands",)
