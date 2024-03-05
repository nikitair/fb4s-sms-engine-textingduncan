from .logging_config import logger
from static import texts
from utils.utils import notify_team_by_email


def log_server_start():
    logger.info("")
    logger.info("=== SERVER STARTED ===\n")
    logger.info(f"{texts.app_logo1}\n")


def log_server_stop():
    logger.info("")
    logger.info("=== SERVER SHUT DOWN ===\n")
    notify_team_by_email("Server Stopped")
