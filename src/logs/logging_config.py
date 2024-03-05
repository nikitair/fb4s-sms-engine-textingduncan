import logging
from datetime import datetime


class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.utcfromtimestamp(record.created)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + ' UTC'


# Logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Custom UTC formatter
formatter = UTCFormatter('%(asctime)s - %(levelname)s - %(message)s')

# Terminal output
th = logging.StreamHandler()
th.setLevel(logging.INFO)
th.setFormatter(formatter)
logger.addHandler(th)

# File output
log_filename = datetime.utcnow().strftime('logs/logs.log')
fh = logging.FileHandler(log_filename)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)
