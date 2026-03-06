import json
import typing
import difflib

from ..core.config import config


class RawCommand(typing.TypedDict):
    keywords: list[str]
    exec: str


class CommandMatcher:
    def __init__(self, commands_list_path: str = config.commands_list_path):
        self._commands_list_path = commands_list_path
        self._commands_list: list[RawCommand] = self._load_commands_list()

    def match_command(self, text: str) -> RawCommand | None:
        if not text:
            raise ValueError("Text is empty")

        keywords = text.split(" ")
        best_match = None
        max_matches = 0
        for raw_command in self._commands_list:
            matches = sum(
                difflib.SequenceMatcher(keyword1, keyword2).ratio() > 0.9
                for keyword1 in keywords
                for keyword2 in raw_command["keywords"]
            )

            if matches > max_matches:
                best_match = raw_command

        return best_match

    def _load_commands_list(self) -> dict:
        return json.load(self._commands_list_path)

    @property
    def commands_list(self):
        return self._commands_list


__all__ = (
    "CommandMatcher",
    "RawCommand",
)
