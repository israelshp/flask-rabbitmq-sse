import logging
import sys


LOG_LEVEL = logging.DEBUG


logger = logging.getLogger("sse")

log_format = "%(asctime)s [%(levelname)s] [%(name)s] [%(threadName)s] %(message)s (%(filename)s:%(lineno)d)"

logger.setLevel(LOG_LEVEL)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


for handler in logger.handlers:
    handler.setFormatter(logging.Formatter(log_format))
    handler.setLevel(LOG_LEVEL)
