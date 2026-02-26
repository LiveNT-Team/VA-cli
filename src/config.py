import typing
import pathlib
import os
import configparser
from exceptions import InvalidDefaultConfigPath, InvalidOverrideConfigPath

DEFAULT_CONFIG_FILE_CONTENT = """
[voice-assistant]
commands-database-path = .local/voice-assistant/commands.db
activation-volume = -30
vosk-model-path = .local/voice-assistant/vosk-model-ru-0.42
samplerate = 48000
channels = 2
lull-duration-sec = 1
device = null
"""
"""Default content of default config file"""


class AppConfig:
    def __init__(
        self,
        *,
        default_config_path: typing.Union[str, pathlib.Path],
        override_config_path: typing.Union[str, pathlib.Path],
        default_config_default_content: str = DEFAULT_CONFIG_FILE_CONTENT,
        override_config_default_content: str = "",
        create_if_not_exists: bool = False,
    ):
        """
        Loads configs from paths

        :param default_config_path:
            - Added in 1.0
        :param override_config_path:
            - Added in 1.0
        :param create_if_not_exists:
            If true, if one of the paths does not exist, it creates one recursive.
            If false, code will raise exception
        :raise InvalidDefaultConfigPath:
            `default_config_path` is not exists
        :raise InvalidOverrideConfigPath:
            `override_config_path` is not exists
        """
        self._default_config_default_content = default_config_default_content
        self._override_config_default_content = override_config_default_content
        self._create_if_not_exists = create_if_not_exists
        self._default_config_path = self._path(default_config_path).absolute()
        self._override_config_path = self._path(override_config_path).absolute()

        self._parser = configparser.ConfigParser()
        self._check_configs_paths()
        self._load_config()

    # region Methods

    def _path(self, path: typing.Union[str, pathlib.Path]):
        """If path is not instance of pathlib.Path, converts it to pathlib.Path"""
        if isinstance(path, pathlib.Path):
            return path
        else:
            return pathlib.Path(path)

    def _check_configs_paths(self):
        """Checks configs paths for exist"""
        for path, default_content, exception in zip(
            (
                self._default_config_path,
                self._override_config_path,
            ),
            (
                self._default_config_default_content,
                self._override_config_default_content,
            ),
            (
                InvalidDefaultConfigPath,
                InvalidOverrideConfigPath,
            ),
        ):
            if not path.exists() or not path.is_file():
                if self._create_if_not_exists:
                    os.makedirs(path.parent, exist_ok=True)
                    with open(path, "w") as file:
                        file.write(default_content)
                else:
                    raise exception(self._default_config_path)

    def _load_config(self):
        """Loads config from config files to self._parser"""
        self._parser.read(
            [
                self._default_config_path,
                self._override_config_path,
            ]
        )

    # endregion

    # region Properties

    @property
    def commands_database_path(self) -> str:
        return self._parser.get("voice-assistant", "commands-database-path")

    @property
    def activation_volume(self) -> int:
        return int(self._parser.get("voice-assistant", "activation-volume"))

    @property
    def vosk_model_path(self) -> str:
        return self._parser.get("voice-assistant", "vosk-model-path")

    @property
    def samplerate(self) -> int:
        return int(self._parser.get("voice-assistant", "samplerate"))

    @property
    def channels(self) -> int:
        return int(self._parser.get("voice-assistant", "channels"))

    @property
    def lull_duration_sec(self) -> int:
        return int(self._parser.get("voice-assistant", "lull-duration-sec"))

    @property
    def device(self) -> int:
        return int(self._parser.get("voice-assistant", "device"))

    # endregion


config = AppConfig(
    default_config_path=".config/voice-assistant/default.ini",
    override_config_path=".config/voice-assistant/override.ini",
    create_if_not_exists=True,
)
__all__ = ("config",)
