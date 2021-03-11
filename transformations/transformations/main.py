from loguru import logger
from pyspark.sql import SparkSession

from transformations.core import FeatureGroupJob
from transformations.definitions import catalog


def spark_session(app_name: str) -> SparkSession:
    return (
        SparkSession
        .builder
        .appName(app_name)
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1")
        .getOrCreate()
    )


def start_transformation_jobs():
    spark = spark_session("Transformations")

    for feature_group in catalog.feature_groups:
        logger.info(f"Starting transformation {feature_group}")
        FeatureGroupJob(spark, feature_group).run()

    spark.streams.awaitAnyTermination()
