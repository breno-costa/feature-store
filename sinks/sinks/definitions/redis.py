from pyspark.sql import SparkSession
from pyspark.sql import DataFrame

from sinks import settings


class RedisSink:
    def __init__(self, spark: SparkSession, schema: str):
        self.spark = spark
        self.schema = schema

    def get_sink_name(self):
        return f"sink-redis-{self.schema}"

    def foreach_batch(self, batch_df: DataFrame, batch_id: int):
        (
            batch_df
            .selectExpr("CAST(key as STRING)", "CAST(value AS STRING) as record")
            .write
            .format("org.apache.spark.sql.redis")
            .mode("overwrite")
            .option("table", self.schema)
            # .option("model", "binary")
            .option("key.column", "key")
            .save()
        )

    def run(self):
        df = (
            self.spark
            .readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", settings.KAFKA_BROKER)
            .option("subscribe", self.schema)
            .load()
        )

        query = (
            df
            .writeStream
            .queryName(self.get_sink_name())
            .outputMode("update")
            .foreachBatch(self.foreach_batch)
            .start()
        )

        return query
