import json
import gzip
from typing import Dict, Any
from datetime import datetime

from loguru import logger
from kafka import KafkaProducer

from producer import settings


def on_send_error(excp: Exception):
    logger.error(f"Error to send record to kafka", exc_info=excp)


def open_file(filepath: str):
    if filepath.endswith("gz"):
        return gzip.open(filepath)
    return open(filepath)


def get_record(line: str, filetype: str):
    try:
        return json.loads(line)
    except Exception as e:
        logger.error(f"Record: {line}")
        logger.error(f"Error to parse record from json - {e}")
        return None


def get_key(record: Dict[str, Any], entity_key: str = None):
    """Get key field from the record to be used as kafka key"""
    if entity_key in record:
        return record.get(entity_key)
    return None


def get_timestamp_ms(record: Dict,
                     timestamp_field: str = None,
                     timestamp_format: str = None):
    """Get timestamp field from the record and convert to unix time"""
    if timestamp_field and timestamp_format and timestamp_field in record:
        timestamp = datetime.strptime(record[timestamp_field],
                                      timestamp_format)
        return int(timestamp.timestamp())
    return None


def get_topic_name(entity: str) -> str:
    return f"entity-{entity}"


def run(filepath: str, filetype: str, entity: str, entity_key: str = None,
        timestamp_field: str = None, timestamp_format: str = None,
        limit: int = None) -> int:

    # TODO: register schema on the registry before sending to kafka
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER,
        api_version=(2, 4, 0),
        acks=settings.KAFKA_ACKS,
        compression_type=settings.KAFKA_COMPRESSION_TYPE,
        key_serializer=str.encode,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    with open_file(filepath) as f:
        for line_number, line in enumerate(f, start=1):
            record = get_record(line, filetype)
            if record is None:
                continue

            producer.send(
                topic=get_topic_name(entity),
                key=get_key(record, entity_key),
                value=record,
                headers=None,
                timestamp_ms=get_timestamp_ms(
                    record,
                    timestamp_field,
                    timestamp_format
                )
            ).add_errback(on_send_error)

            if line_number % 1000 == 0:
                logger.info(f"[entity: {entity}] {line_number} lines were processed")

            if limit and line_number == limit:
                break

    return line_number
