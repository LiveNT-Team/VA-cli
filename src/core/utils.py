import random
import string
import numpy

id_symbols = string.ascii_letters + string.digits


def generate_voice_command_id(length: int = 10) -> str:
    id = ""
    while length > 0:
        id += str(random.choice(id_symbols))
        length -= 1
    return id


def get_dbfs_volume(audio: numpy.ndarray) -> float:
    """Returns volume of audio in dbfs"""
    rms = numpy.sqrt(numpy.mean(audio**2))
    return 20 * numpy.log10(rms) if rms > 0 else float("-inf")


__all__ = (
    "generate_voice_command_id",
    "get_dbfs_volume",
)
