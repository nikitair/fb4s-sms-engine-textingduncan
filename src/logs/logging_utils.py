from .logging_config import logger
from static import texts


def log_server_start():
    logger.info("")
    logger.info("=== SERVER STARTED ===\n")
    logger.info(f"{texts.app_logo}\n")


def log_server_stop():
    logger.info("")
    logger.info("=== SERVER SHUT DOWN ===\n")
