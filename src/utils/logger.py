"""
Structured logging for the AI Math Solver.

WHY THIS PATTERN:
- Python's built-in logging module is powerful but verbose to set up
- This module gives every file a pre-configured logger with ONE line:
      from src.utils import get_logger
      logger = get_logger(__name__)
- Logs include: timestamp, module name, level, and message
- Log level is controlled from settings.py (via .env)

PRODUCTION BENEFIT:
- When debugging a pipeline failure, you can trace exactly which agent
  failed and what data it received — without adding print() everywhere
"""

import logging
import sys

from src.config import settings


def get_logger(name: str) -> logging.Logger:
    """
    Create a configured logger for a module.

    Args:
        name: Usually __name__ — gives you the module path (e.g. 'src.vision.ocr')

    Returns:
        A logger instance with console output and proper formatting.

    Usage:
        logger = get_logger(__name__)
        logger.info("OCR extracted: %s", text)
        logger.error("Failed to parse: %s", raw, exc_info=True)
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if get_logger is called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    # Console handler — all logs go to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    # Format: 2026-03-16 11:20:00 | INFO | src.vision.ocr | Extracted text: x^2 + 3x
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Don't propagate to root logger (avoids duplicate messages)
    logger.propagate = False

    return logger
