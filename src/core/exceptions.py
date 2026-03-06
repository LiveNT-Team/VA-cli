class VACLIExp(Exception):
    pass


class InvalidDefaultConfigPath(VACLIExp):
    """Raises if default config path is invalid"""

    def __init__(self, path):
        super().__init__("Invalid default config path")
        self.path = path


class InvalidOverrideConfigPath(VACLIExp):
    """Raises if override config path is invalid"""

    def __init__(self, path):
        super().__init__("Invalid override config path")
        self.path = path


class InvalidVoskModelPath(VACLIExp):
    """Raises if vosk model path is invalid"""

    def __init__(self):
        super().__init__("Invalid vosk model path")


__all__ = (
    "InvalidDefaultConfigPath",
    "InvalidOverrideConfigPath",
    "InvalidVoskModelPath",
)
