import io
import json
import wave
import vosk
import os
import numpy
import logging

from ..core.exceptions import InvalidVoskModelPath
from ..core.config import config


logger = logging.getLogger()


class SpeechRecognitionResult:
    """Type for speech recognition result"""

    def __init__(self, *, text: str, **kwargs):
        super().__init__()
        self._text = text

    @property
    def text(self):
        """The text property."""
        return self._text


class SpeechRecognizer:
    def __init__(
        self,
        vosk_model_path: str = config.vosk_model_path,
        samplerate: int = config.samplerate,
        channels: int = config.channels,
    ):
        self._model = self._load_model(vosk_model_path)
        self._samplerate = samplerate
        self._channels = channels

    def _load_model(self, path: str) -> vosk.Model:
        if os.path.exists(path) and os.path.isdir(path):
            logger.debug(f"Loading vosk model from {path}")
            model = vosk.Model(config.vosk_model_path)
            logger.debug(f"Successfully loaded vosk model from {path}")
            return model

        raise InvalidVoskModelPath()

    def recognize_speech(self, audio_float32: numpy.ndarray) -> SpeechRecognitionResult:
        """
        Accepts a ndarray with type float32 and recognize

        :param audio_float32:
            Audio array in float32
        :return SpeechRecognitionResult:

        To get text, use string key

        >>> result = recognize_speech(...)
        >>> result["text"]
        <text>
        """
        logger.debug("Recognizing speech")
        # Converting in int16
        audio_int16 = (audio_float32 * 32767).astype(numpy.int16)
        wav_buffer = io.BytesIO()
        with wave.Wave_write(wav_buffer) as wav:
            wav.setframerate(self._samplerate)
            wav.setnchannels(self._channels)
            wav.setsampwidth(2)
            wav.writeframes(audio_int16)

        wav_buffer.seek(0)
        with wave.Wave_read(wav_buffer) as wav:
            rec = vosk.KaldiRecognizer(self._model, wav.getframerate())
            rec.SetWords(True)
            while True:
                data = wav.readframes(4000)
                if len(data) == 0:
                    break

                rec.AcceptWaveform(data)
                logger.debug(rec.PartialResult())

            result = json.loads(rec.FinalResult())
            return SpeechRecognitionResult(**result)


__all__ = ("SpeechRecognizer",)
