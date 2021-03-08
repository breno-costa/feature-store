from loguru import logger

from feature_store import settings
from feature_store.features import status


def run():
    logger.info("KAFKA_BROKER:")
    logger.info(settings.KAFKA_BROKER)

    status.run()
