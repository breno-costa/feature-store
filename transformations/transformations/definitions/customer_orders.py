from dataclasses import dataclass

from pyspark.sql import DataFrame
from pyspark.sql import functions as f

from transformations.core import FeatureGroup


@dataclass
class CustomerOrdersOnLastDay(FeatureGroup):
    name: str = "customer_orders_on_last_day"
    key: str = "customer_id"
    input_entity: str = "order"
    output_entity: str = "customer"

    def transform(self, order_df: DataFrame) -> DataFrame:
        return (
            order_df
            .where(f.col("customer_id").isNotNull())
            .groupBy(
                f.col("customer_id"),
                f.window(f.col("order_created_at"), "1 day")
            )
            .agg(
                f.count("order_id").alias("number_orders_1d"),
                f.avg("order_total_amount").alias("avg_ticket_price_1d")
            )
            .select(
                "customer_id", "number_orders_1d", "avg_ticket_price_1d"
            )
        )
