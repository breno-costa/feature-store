from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType
from pyspark.sql.functions import col, from_json, to_json, struct

from feature_store import settings
from feature_store.registry import schemas


def get_schema(schema: str) -> StructType:
    return StructType.fromJson(schemas.get_schema(schema))


def from_kafka(df: DataFrame, schema: str) -> DataFrame:
    return (
        df
        .selectExpr("CAST(key as STRING)", "CAST(value AS STRING)")
        .withColumn("record", from_json(col("value"), get_schema(schema)))
        .select("key", "record.*")
    )


def to_kafka(df: DataFrame, key_field: str) -> DataFrame:
    return df.select(
        col(key_field).alias("key"),
        to_json(struct([df[x] for x in df.columns])).alias("value")
    )


def run():
    input_schema = "event-status"
    output_schema = "feature-status"
    key_field = "status_id"

    spark = (
        SparkSession.builder
        .appName("StructuredStreaming")
        .getOrCreate()
    )

    # Subscribe to kafka topic
    df = (
        spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", settings.KAFKA_BROKER)
        .option("subscribe", input_schema)
        .load()
    )

    # Flattening value field
    df = from_kafka(df, input_schema)

    # Start running the query
    query = (
        to_kafka(df, key_field)
        .writeStream
        .outputMode("update")
        .format("kafka")
        .option("kafka.bootstrap.servers", settings.KAFKA_BROKER)
        .option("topic", output_schema)
        .option("checkpointLocation", "checkpointPath")
        .start()
    )

    query.awaitTermination()
