from components.listener import InputStream
from numpy import save
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def callback(audio):
    save("test.npy", audio)


listener = InputStream(callback)
listener.start_listening()
