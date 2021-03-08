import os
import json
from typing import Dict

from loguru import logger


def get_filename(schema_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), f"{schema_name}.json")


def get_schema(schema_name: str) -> Dict:
    with open(get_filename(schema_name)) as f:
        logger.info(f.name)
        return json.load(f)
