class VACLIExp(Exception):
    pass


class InvalidDefaultConfigPath(VACLIExp):
    def __init__(self, path):
        super().__init__("Invalid default config path")
        self.path = path


class InvalidOverrideConfigPath(VACLIExp):
    def __init__(self, path):
        super().__init__("Invalid override config path")
        self.path = path


class FailedToLoadVoskModel(VACLIExp):
    def __init__(self):
        super().__init__("Invalid vosk model path")


__all__ = (
    "InvalidDefaultConfigPath",
    "InvalidOverrideConfigPath",
    "FailedToLoadVoskModel",
)
