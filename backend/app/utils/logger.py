"""Logging configuration and utilities"""

import logging
import sys
from typing import Optional
import os


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Setup and configure logger
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (INFO, DEBUG, WARNING, ERROR). 
               If None, uses LOG_LEVEL env var or defaults to INFO
    
    Returns:
        Configured logger instance
    """
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    logger = logging.getLogger(name)
    log_level = getattr(logging, level, logging.INFO)
    logger.setLevel(log_level)
    
    if logger.handlers:
        return logger
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return setup_logger(name)

