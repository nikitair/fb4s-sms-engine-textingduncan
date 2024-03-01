from .logging_config import logger


def log_server_start():
    logger.info("")
    logger.info("=== SERVER STARTED ===\n")


def log_server_stop():
    logger.info("")
    logger.info("=== SERVER SHUT DOWN ===\n")
