"""
Centralized logging configuration.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from config import settings


settings.logs_dir.mkdir(
    parents=True,
    exist_ok=True,
)


LOG_FILE = settings.logs_dir / "docmind.log"


def get_logger(name: str = "docmind") -> logging.Logger:
    """
    Create and return a configured logger.

    Parameters
    ----------
    name:
        Logger name.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level.upper())

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger