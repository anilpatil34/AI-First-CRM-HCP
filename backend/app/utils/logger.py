"""
Structured logging configuration.
Provides consistent log formatting across the application.
"""

import logging
import sys
from datetime import datetime, timezone


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for console."""

    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[41m",  # Red background
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        record.asctime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger with colored console output.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        formatter = ColoredFormatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
