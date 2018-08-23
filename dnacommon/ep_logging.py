import logging

import sys

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARN = logging.WARN
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

_logging_nameToLevel = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}


def name_as_level(name: str):
    if name is not None:
        return _logging_nameToLevel.get(name.upper(), "INFO")
    else:
        return "INFO"


def get_logger(name, loglevel=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    logger.propagate = False
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(loglevel)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    pass
