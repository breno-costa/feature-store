import pytest

from pyspark.sql import SparkSession


@pytest.fixture
def spark_session():
    return (
        SparkSession
        .builder
        .appName("definitions")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1")
        .getOrCreate()
    )
