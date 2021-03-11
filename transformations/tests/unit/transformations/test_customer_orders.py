import pytest

from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import StringType, LongType, FloatType, DoubleType

from transformations.utils import are_dfs_equal
from transformations.definitions.customer_orders import CustomerOrdersOnLastDay


def get_order_df(spark_session):
    """
+--------------------+--------------------+------------------+--------------------+
|         customer_id|            order_id|order_total_amount|    order_created_at|
+--------------------+--------------------+------------------+--------------------+
|9947c352-afb7-46f...|c611ba64-1d01-4c3...|              34.0|2019-01-01T15:45:...|
|9947c352-afb7-46f...|4529c9ac-6a47-485...|              49.0|2019-01-01T21:50:...|
|9947c352-afb7-46f...|a59203d5-5d99-46b...|              40.0|2019-01-01T14:02:...|
|e1e4733f-42d5-4f3...|2b6547d1-f7ea-476...|              29.8|2019-01-18T23:32:...|
|e1e4733f-42d5-4f3...|5ce59c48-fa46-416...|              15.9|2019-01-18T23:41:...|
+--------------------+--------------------+------------------+--------------------+
    """
    data = [
        Row(customer_id='9947c352-afb7-46f3-8ebd-93975bb7d396',
            order_id='a59203d5-5d99-46b4-ade9-deb9661a47bb',
            order_total_amount=40.0,
            order_created_at='2019-01-01T14:02:40.000Z'),
        Row(customer_id='9947c352-afb7-46f3-8ebd-93975bb7d396',
            order_id='c611ba64-1d01-4c32-9444-0f356c14c393',
            order_total_amount=34.0,
            order_created_at='2019-01-01T15:45:52.000Z'),
        Row(customer_id='9947c352-afb7-46f3-8ebd-93975bb7d396',
            order_id='4529c9ac-6a47-485a-8916-21be8d57dbd1',
            order_total_amount=49.0,
            order_created_at='2019-01-01T21:50:25.000Z'),
        Row(customer_id='e1e4733f-42d5-4f35-a757-e59667cd4422',
            order_id='2b6547d1-f7ea-4763-b1a4-07cae87efbd5',
            order_total_amount=29.8,
            order_created_at='2019-01-18T23:32:08.000Z'),
        Row(customer_id='e1e4733f-42d5-4f35-a757-e59667cd4422',
            order_id='5ce59c48-fa46-416a-906f-239cf5fec8a4',
            order_total_amount=15.9,
            order_created_at='2019-01-18T23:41:45.000Z')
    ]
    schema = StructType([
        StructField("customer_id", StringType()),
        StructField("order_id", StringType()),
        StructField("order_total_amount", FloatType()),
        StructField("order_created_at", StringType())
    ])
    return spark_session.createDataFrame(data, schema)


def get_customer_orders_df(spark_session):
    """
+--------------------+----------------+-------------------+
|         customer_id|number_orders_1d|avg_ticket_price_1d|
+--------------------+----------------+-------------------+
|9947c352-afb7-46f...|               3|               41.0|
|e1e4733f-42d5-4f3...|               2|  22.84999942779541|
+--------------------+----------------+-------------------+
    """
    data = [
        Row(customer_id='9947c352-afb7-46f3-8ebd-93975bb7d396',
            number_orders_1d=3,
            avg_ticket_price_1d=41.0),
        Row(customer_id='e1e4733f-42d5-4f35-a757-e59667cd4422',
            number_orders_1d=2,
            avg_ticket_price_1d=22.84999942779541)
    ]
    schema = StructType([
        StructField("customer_id", StringType()),
        StructField("number_orders_1d", LongType()),
        StructField("avg_ticket_price_1d", DoubleType())
    ])
    return spark_session.createDataFrame(data, schema)


def test_customer_orders(spark_session):
    order_df = get_order_df(spark_session)
    features_df = CustomerOrdersOnLastDay().transform(order_df)
    expected_df = get_customer_orders_df(spark_session)

    assert features_df.count() == 2
    assert are_dfs_equal(features_df, expected_df)
