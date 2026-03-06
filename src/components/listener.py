import sounddevice
import typing
import numpy
import logging

from ..core.config import config
from ..core.utils import get_dbfs_volume

logger = logging.getLogger()


class InputStream:
    def __init__(
        self,
        callback: typing.Callable[[numpy.ndarray]],
        samplerate: int = config.samplerate,
        channels: int = config.channels,
    ):
        self._audio = numpy.empty((0, config.channels), dtype=numpy.float32)
        self._callback = callback
        self._samplerate = samplerate
        self._channels = channels
        self._is_listening = False

    def start_listening(self):
        self._is_listening = True

        def callback(audio: numpy.ndarray, frames, time, status):
            volume = get_dbfs_volume(audio)
            logger.debug(f"Input volume: {volume}")
            if volume > config.activation_volume:
                self._audio = numpy.vstack([self._audio, audio])
            else:
                if self._audio.size > 0:
                    logger.debug("Calling listener callback")
                    self._callback(self._audio)

                self._audio = numpy.empty((0, config.channels), dtype=numpy.float32)

        with sounddevice.InputStream(
            samplerate=config.samplerate,
            blocksize=config.samplerate * config.lull_duration_sec,
            device=config.device,
            channels=config.channels,
            callback=callback,
        ):
            logger.debug("Listening...")
            while self._is_listening:
                pass

    def __enter__(self):
        self.start_listening()

    def __exit__(self, exc_type, exc, tb):
        self.stop_listening()

    def stop_listening(self):
        self._is_listening = False
        logger.debug("Stopped listening")


__all__ = ("InputStream",)
