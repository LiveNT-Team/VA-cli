import io
import json
import wave
import vosk
import os
import numpy
import logging

from core.exceptions import InvalidVoskModelPath
from core.config import Config


logger = logging.getLogger(__name__)


class SpeechRecognizer:
    def __init__(self, config: Config):
        self._config = config
        self._model = self._load_model()

    def _load_model(self) -> vosk.Model:
        if os.path.exists(self._config.vosk_model_path):
            logger.debug(f"Loading vosk model from {self._config.vosk_model_path}")
            model = vosk.Model(self._config.vosk_model_path)
            logger.debug(
                f"Successfully loaded vosk model from {self._config.vosk_model_path}"
            )
            return model

        raise InvalidVoskModelPath()

    def recognize_speech(self, audio_float32: numpy.ndarray) -> str:
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
            wav.setframerate(self._config.samplerate)
            wav.setnchannels(self._config.channels)
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

            result = json.loads(rec.FinalResult())
            logger.debug(f"Recognized text: {result["text"]}")
            return result["text"]


__all__ = ("SpeechRecognizer",)
