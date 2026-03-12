import json
import os
import subprocess
import typing
import difflib
import logging

from core.config import config

logger = logging.getLogger(__file__)


class RawCommand(typing.TypedDict):
    name: str = ""
    description: str = ""
    shell: bool = True
    phrase: str
    exec: str


class RawCommandQueryResult:
    def __init__(self, ratio: float, raw_command: RawCommand | None):
        self._ratio = ratio
        self._raw_command = raw_command

    @property
    def ratio(self):
        return self._ratio

    @property
    def raw_command(self):
        return self._raw_command

    def __repr__(self):
        return f"{self.__class__.__qualname__}(ratio={self.ratio}, command_name={self.raw_command["name"]})"


class CommandsCRUD:
    def __init__(self, commands_list_path: str = config.commands_list_path):
        self._commands_list_path = commands_list_path
        self._commands_list: list[RawCommand] = self._load_commands_list()

    def query_raw_command(self, text: str) -> RawCommandQueryResult:
        """
        :raises ValueError: if text is empty
        """
        if not text:
            raise ValueError("Text is empty")

        best_ratio = None
        max_ratio = 0.0
        for raw_command in self._commands_list["commands"]:
            ratio = difflib.SequenceMatcher(a=text, b=raw_command["phrase"]).ratio()
            if ratio > max_ratio:
                max_ratio = ratio
                best_ratio = raw_command

        result = RawCommandQueryResult(
            ratio=max_ratio,
            raw_command=best_ratio,
        )
        logger.debug(f"Founded command: {result}")

        return result

    def execute_raw_command(self, raw_command: RawCommand):
        logger.info(
            f"Running command: {raw_command["name"]}. Executing: {raw_command["exec"]}"
        )
        subprocess.run(raw_command["exec"], shell=raw_command["shell"])

    def _load_commands_list(self) -> dict[str, list[RawCommand]]:
        if os.path.exists(self._commands_list_path):
            with open(self._commands_list_path, "r") as file:
                return json.loads(file.read())

        else:
            with open(self._commands_list_path, "w") as file:
                file.write(json.dumps({"commands": []}))

            with open(self._commands_list_path, "r") as file:
                return json.loads(file.read())

    @property
    def commands_list(self):
        return self._commands_list


__all__ = (
    "CommandsCRUD",
    "RawCommand",
)
