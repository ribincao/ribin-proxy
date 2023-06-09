import logging
import signal
import sys
import os


class Singleton(object):
    _inst = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._inst, cls):
            cls._inst = object.__new__(cls)
        return cls._inst


LOG_NAME = "shadowsocks"
LOG_MODE_FILE = "file"
LOG_MODE_CONSOLE = "console"
LOG_FORMAT = "%(levelname)s|%(asctime)s|%(message)s"


class Logger(Singleton):

    def __init__(self):
        self._logger: logging.Logger = logging.getLogger(LOG_NAME)
        self.log_mode: str = LOG_MODE_CONSOLE
        self.log_level: str = "INFO"
        self.log_path: str = "server.log"

    def init_logger(self):
        self._logger.setLevel(self.log_level)
        handler = None
        if self.log_mode == LOG_MODE_FILE:
            up_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            handler = logging.FileHandler(up_path + f"/{os.getpid()}-" + self.log_path, encoding="utf-8")

        if self.log_mode == LOG_MODE_CONSOLE:
            handler = logging.StreamHandler(sys.stdout)

        if not handler:
            return

        handler.setLevel(level=self.log_level)
        log_format = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(log_format)

        self._logger.addHandler(handler)

    @staticmethod
    def format_msg(msg):
        try:
            caller = sys._getframe(1)
            file_name = '/'.join(caller.f_code.co_filename.split('/')[-3:])
            call_name, file_no = caller.f_code.co_name, caller.f_lineno
            return ':'.join([file_name, call_name, str(file_no)]) + f'|{msg}'
        except Exception as e:
            return msg

    def debug(self, msg: str):
        msg = self.format_msg(msg)
        if self.log_mode == LOG_MODE_CONSOLE:
            msg = f"\033[34m{msg}\033[0m"
        self._logger.debug(msg)

    def info(self, msg: str):
        msg = self.format_msg(msg)
        if self.log_mode == LOG_MODE_CONSOLE:
            msg = f"\033[32m{msg}\033[0m"
        self._logger.info(msg)

    def warning(self, msg: str):
        msg = self.format_msg(msg)
        if self.log_mode == LOG_MODE_CONSOLE:
            msg = f"\033[33m{msg}\033[0m"
        self._logger.warning(msg)

    def error(self, msg: str):
        msg = self.format_msg(msg)
        if self.log_mode == LOG_MODE_CONSOLE:
            msg = f"\033[31m{msg}\033[0m"
        self._logger.error(msg, stack_info=True)


def signal_handler():
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    def receive_signal(signum, stack):
        logger.warning(f"Program exit {signum} {stack}")
        exit(-1)
    signal.signal(signal.SIGQUIT, receive_signal)
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGABRT, receive_signal)
    signal.signal(signal.SIGSEGV, receive_signal)


signal_handler()
logger = Logger()

if __name__ == "__main__":
    logger.init_logger()
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")


