from configparser import ConfigParser

DEFAULT_VOICE_COMMAND_ID_LENGTH = 16


class Config:
    def __init__(
        self,
        config_path: str,
        default_config_path: str = "./default_config.ini",
    ):
        self._config_parser = ConfigParser()
        self._config_parser.read([config_path, default_config_path])
        self.activation_volume = self._config_parser.getfloat(
            "voice", "activation_volume"
        )
        self.lull_duration_sec = self._config_parser.getint(
            "voice", "lull_duration_sec"
        )
        self.device = self._config_parser.getint("voice", "device")
        self.use_default_device = self._config_parser.getboolean(
            "voice", "use_default_device"
        )
        self.channels = self._config_parser.get("voice", "channels")
        self.samplerate = self._config_parser.get("voice", "samplerate")

        self.vosk_model_path = self._config_parser.get("vosk", "model_path")

        self.voice_commands_list_filename = self._config_parser.get(
            "assistant", "voice_commands_list_filename"
        )
        self.minimal_sequence_ratio = self._config_parser.get(
            "assistant", "minimal_sequence_ratio"
        )


__all__ = ("Config",)
