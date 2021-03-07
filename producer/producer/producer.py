import json
import gzip
from typing import Dict, Any
from datetime import datetime

from loguru import logger
from kafka import KafkaProducer


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


def get_key(record: Dict[str, Any], key_field: str = None):
    if key_field in record:
        return record.get(key_field)
    return None


def get_timestamp_ms(record: Dict, timestamp_field: str = None,
                     timestamp_format: str = None):
    if timestamp_field and timestamp_format and timestamp_field in record:
        timestamp = datetime.strptime(record[timestamp_field],
                                      timestamp_format)
        return int(timestamp.timestamp())
    return None


def run(filepath: str, filetype: str, topic: str, key_field: str = None,
        timestamp_field: str = None, timestamp_format: str = None) -> int:

    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        api_version=(2, 4, 0),
        acks="all",
        compression_type="gzip",
        key_serializer=str.encode,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    with open_file(filepath) as f:
        for line_number, line in enumerate(f):
            record = get_record(line, filetype)
            if record is None:
                continue

            producer.send(
                topic=topic,
                key=get_key(record, key_field),
                value=record,
                headers=None,
                timestamp_ms=get_timestamp_ms(
                    record,
                    timestamp_field,
                    timestamp_format
                )
            ).add_errback(on_send_error)

            if line_number % 1000 == 0:
                logger.info(f"Producer: {line_number} lines were processed")

    return line_number + 1
