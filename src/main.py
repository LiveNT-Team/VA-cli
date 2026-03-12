from components.listener import InputStream
from components.speech_recognizer import SpeechRecognizer
from components.commands_crud import CommandsCRUD
from core.config import config
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class VA:
    def __init__(self):
        self._speech_recognizer = SpeechRecognizer()
        self._commands_crud = CommandsCRUD()
        self._listener = InputStream(self._callback)

    def _callback(self, audio):
        sr_result = self._speech_recognizer.recognize_speech(audio)
        try:
            cmd_query_result = self._commands_crud.query_raw_command(sr_result.text)
        except ValueError:
            pass
        else:
            if cmd_query_result.ratio <= config.keywords_sequence_minimal_ratio:
                logger.info("Command was not found")
                return

            self._commands_crud.execute_raw_command(cmd_query_result.raw_command)

    def start(self):
        self._listener.start_listening()


va = VA()
va.start()
