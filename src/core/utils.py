import numpy


def get_dbfs_volume(audio: numpy.ndarray) -> float:
    rms = numpy.sqrt(numpy.mean(audio**2))
    return 20 * numpy.log10(rms) if rms > 0 else float("-inf")
