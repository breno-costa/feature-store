from loguru import logger
from pyspark.sql import SparkSession

from sinks import catalog
from sinks import settings
from sinks.definitions.redis import RedisSink


def spark_session(app_name: str) -> SparkSession:
    return (
        SparkSession
        .builder
        .appName(app_name)
        .config("spark.jars.packages", "com.redislabs:spark-redis_2.12:2.6.0")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1")
        .config("spark.ui.port", settings.SPARK_UI_PORT)
        .config("spark.redis.host", settings.REDIS_HOST)
        .config("spark.redis.port", settings.REDIS_PORT)
        .getOrCreate()
    )


def start_sink_jobs():
    spark = spark_session("Sinks")

    for schema in catalog.schemas:
        logger.info(f"Starting sink: {schema}")
        RedisSink(spark=spark, feature_group=feature_group).run()

    spark.streams.awaitAnyTermination()
