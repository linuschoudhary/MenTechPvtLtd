import logging
# import os
# os.makedirs("Log",exist_ok=True)


logging.basicConfig(
    filename="Log/activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

logging.getLogger("watchfiles").setLevel(logging.CRITICAL)
logging.getLogger("watchfiles.main").setLevel(logging.CRITICAL)

logger=logging.getLogger(__name__)