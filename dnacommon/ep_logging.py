import logging
import time
import sys
from datetime import datetime, timezone

_logging_nameToLevel = {
    "CRITICAL": logging.CRITICAL,
    "FATAL": logging.FATAL,
    "ERROR": logging.ERROR,
    "WARN": logging.WARNING,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


def name_as_level(name: str) -> int:
    return (
        _logging_nameToLevel.get(name.upper(), logging.INFO)
        if name is not None
        else logging.INFO
    )


class EpFormatter(logging.Formatter):
    converter = datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created, tz=timezone.utc)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s


def get_logger(name, loglevel=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    logger.propagate = False
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(loglevel)
        formatter = EpFormatter(
            "[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S.%f%z",
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

