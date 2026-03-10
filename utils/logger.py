"""NeuroAgent – Logging utilities."""

import logging
import os
from logging.handlers import TimedRotatingFileHandler


LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger that writes to both console and a daily rotating log file."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler – INFO and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler – daily rotation, keeps 30 days of logs
    log_file = os.path.join(LOG_DIR, "neuroagent.log")
    fh = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
