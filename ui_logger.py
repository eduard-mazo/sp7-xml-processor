# logger.py
import sys
import logging


class StreamToLogger:
    """
    Redirige sys.stdout y sys.stderr al logger
    """

    def __init__(self, log_callback):
        self.log_callback = log_callback

    def write(self, message):
        message = message.strip()
        if message:
            self.log_callback(message)

    def flush(self):
        pass


# Logger global para integrar con GUI
class UILogger:
    def __init__(self):
        self._callback = print  # fallback por defecto
        self._stream_redirected = False

    def set_callback(self, callback):
        self._callback = callback
        self._redirect_stdout()

    def _redirect_stdout(self):
        if not self._stream_redirected:
            sys.stdout = StreamToLogger(self._callback)
            sys.stderr = StreamToLogger(self._callback)
            self._stream_redirected = True

    def log(self, msg):
        self._callback(msg)


# Instancia global
ui_logger = UILogger()

# Setup del módulo logging (para usar logger.info() etc.)
logger = logging.getLogger("sp7_logger")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
