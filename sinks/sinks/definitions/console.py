from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from sinks import settings


class ConsoleSink:
    def __init__(self, spark: SparkSession, feature_group: str):
        self.spark = spark
        self.feature_group = feature_group

    def get_sink_name(self):
        return f"sink-console-{self.feature_group}"

    def run(self):
        df = (
            self.spark
                .readStream
                .format("kafka")
                .option("kafka.bootstrap.servers", settings.KAFKA_BROKER)
                .option("subscribe", self.feature_group)
                .load()
        )

        df = (
            df
            .selectExpr("CAST(key as STRING)", "CAST(value AS STRING)")
            .select(col("key").alias("_id"), col("value"))
        )

        query = (
            df
            .writeStream
            .queryName(self.get_sink_name())
            .outputMode("update")
            .format("console")
            .option("truncate", "false")
            .start()
        )

        return query
