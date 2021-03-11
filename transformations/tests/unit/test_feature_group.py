from pyspark.sql import DataFrame
from pyspark.sql import functions as f

from transformations import core
from transformations.definitions.order_creation import OrderCreation


JSON_INPUT_PATH = "tests/unit/data/order.json"
JSON_OUTPUT_PATH = "tests/unit/data/order_creation.json"


class MockedFeatureGroupJob(core.FeatureGroupJob):
    def subscribe(self) -> DataFrame:
        schema = self.spark.read.json(JSON_INPUT_PATH).schema
        df = (
            self.spark
            .readStream
            .format("json")
            .schema(schema)
            .load(JSON_INPUT_PATH)
        )
        return df.select(
            f.col("order_id").alias("key"),
            f.to_json(f.struct([c for c in df.columns])).alias("value")
        )

    def start_query(self, df: DataFrame):
        return (
            df
            .writeStream
            .queryName("order")
            .format("memory")
            .option("checkpointLocation", "any")
            .start()
        )


def test_feature_group_job(monkeypatch, spark_session):
    monkeypatch.setattr(core, "FeatureGroupJob", MockedFeatureGroupJob)

    feature_group_job = core.FeatureGroupJob(
        spark=spark_session,
        definition=OrderCreation()
    )

    query = feature_group_job.run()

    assert query
