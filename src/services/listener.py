import sounddevice
import typing
import numpy
import logging
import asyncio
import os
from time import sleep

from core.config import Config
from core.utils import get_dbfs_volume

logger = logging.getLogger(__name__)


class Listener:
    def __init__(
        self,
        config: Config,
        callback: typing.Callable[[numpy.ndarray]],
    ):
        self._config = config
        self._audio = numpy.empty((0, self._config.channels), dtype=numpy.float32)
        self._callback = callback
        self._is_listening = False

    async def start_listening(self):
        loop = asyncio.get_event_loop()
        self._is_listening = True

        def callback(
            audio: numpy.ndarray,
            frames,
            time,
            status,
            loop: asyncio.AbstractEventLoop,
        ):
            volume = get_dbfs_volume(audio)
            logger.debug(f"Input volume: {volume}")
            if volume > self._config.activation_volume:
                self._audio = numpy.vstack([self._audio, audio.copy()])
            else:
                if self._audio.size > 0:
                    logger.debug("Calling listener callback")
                    loop.call_soon_threadsafe(self._callback, self._audio)

                self._audio = numpy.empty(
                    (0, self._config.channels), dtype=numpy.float32
                )

        with sounddevice.InputStream(
            samplerate=self._config.samplerate,
            blocksize=self._config.samplerate * self._config.lull_duration_sec,
            device=None if self._config.use_default_device else self._config.device,
            channels=self._config.channels,
            callback=lambda *args: callback(*args, loop=loop),
        ):
            logger.debug("Listening...")
            while self._is_listening and os.path.exists("active.flag"):
                await asyncio.sleep(1)
            self.stop_listening()

    def stop_listening(self):
        self._is_listening = False
        logger.debug("Stopped listening")

    def __enter__(self):
        self.start_listening()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop_listening()


__all__ = ("Listener",)
