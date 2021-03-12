from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from sinks import settings


class ConsoleSink:
    def __init__(self, spark: SparkSession, schema: str):
        self.spark = spark
        self.schema = schema

    def get_sink_name(self):
        return f"sink-console-{self.schema}"

    def run(self):
        df = (
            self.spark
                .readStream
                .format("kafka")
                .option("kafka.bootstrap.servers", settings.KAFKA_BROKER)
                .option("subscribe", self.schema)
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
