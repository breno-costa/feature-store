from dataclasses import dataclass

from pyspark.sql import DataFrame
from pyspark.sql import functions as f

from transformations.core import FeatureGroup


@dataclass
class OrderCreation(FeatureGroup):
    name: str = "order_creation"
    key: str = "order_id"
    input_entity: str = "order"
    output_entity: str = "order"

    def transform(self, order_df: DataFrame) -> DataFrame:
        return (
            order_df
            .where(f.col("order_created_at").isNotNull())
            .select(
                f.col("order_id"),
                f.year("order_created_at").alias("order_year"),
                f.month("order_created_at").alias("order_month"),
                f.dayofmonth("order_created_at").alias("order_day"),
                f.dayofweek("order_created_at").alias("order_dayofweek"),
                f.dayofyear("order_created_at").alias("order_dayofyear"),
            )
        )
