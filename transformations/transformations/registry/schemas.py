import os
import json
from typing import Dict
from pyspark.sql.types import StructType


def get_filename(full_schema_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), f"{full_schema_name}.json")


def get_schema(full_schema_name: str) -> Dict:
    with open(get_filename(full_schema_name)) as f:
        return json.load(f)


def get_full_schema_name(schema_type: str, schema_name: str) -> str:
    return f"{schema_type}-{schema_name}"


def get_entity_name(schema_name: str) -> str:
    return get_full_schema_name("entity", schema_name)


def get_featuregroup_name(schema_name: str) -> str:
    return get_full_schema_name("featuregroup", schema_name)


def get_spark_schema(full_schema: str) -> StructType:
    return StructType.fromJson(get_schema(full_schema))
