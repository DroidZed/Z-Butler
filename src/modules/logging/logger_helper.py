from typing import Any
from loguru import logger
from utils.singleton_class import SingletonClass


class LoggerHelper(metaclass=SingletonClass):
    def __init__(self) -> None:
        self.log = logger
        self.log.remove(0)
        self.log.add(
            "./logs/bot/file_{time}.log",
            enqueue=True,
            rotation="10 MB",
            backtrace=True,
            diagnose=True,
            compression="zip",
        )

    def info(self, message: str) -> None:
        self.log.info(message)

    def warning(self, message: str) -> None:
        self.log.warning(message)

    def error(self, message: str) -> None:
        self.log.error(message)

    def debug(self, message: str) -> None:
        self.log.debug(message)

    def critical(self, message: str) -> None:
        self.log.critical(message)

    def success(self, message: str) -> None:
        self.log.success(message)

    def exception(self, message: str) -> None:
        self.log.exception(message)
