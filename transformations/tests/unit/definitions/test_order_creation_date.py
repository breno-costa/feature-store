import pytest

from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import StringType, IntegerType

from transformations.utils import are_dfs_equal
from transformations.definitions.order_creation import OrderCreation


def get_order_df(spark_session):
    """
+--------------------+--------------------+
|            order_id|    order_created_at|
+--------------------+--------------------+
|8deafc7f-60df-423...|2019-01-21T00:04:...|
|8f8f3633-0e80-48a...|2019-01-31T23:18:...|
|17c91ae3-1f5e-4a7...|2019-01-08T22:39:...|
|5b8670c0-e2f1-4a6...|2019-01-31T22:15:...|
|71abcdd3-fa2f-4d7...|2019-01-13T01:01:...|
+--------------------+--------------------+
    """
    data = [
        Row(order_id='8deafc7f-60df-4235-9629-db5f9ec82458',
            order_created_at='2019-01-21T00:04:14.000Z'),
        Row(order_id='8f8f3633-0e80-48ae-91a4-2161d9fdda24',
            order_created_at='2019-01-31T23:18:49.000Z'),
        Row(order_id='17c91ae3-1f5e-4a70-8efb-08cf3f8498c4',
            order_created_at='2019-01-08T22:39:55.000Z'),
        Row(order_id='5b8670c0-e2f1-4a66-bc16-553d45dfc848',
            order_created_at='2019-01-31T22:15:24.000Z'),
        Row(order_id='71abcdd3-fa2f-4d75-b5ee-68aa262bfe58',
            order_created_at='2019-01-13T01:01:11.000Z')
    ]
    schema = StructType([
        StructField("order_id", StringType()),
        StructField("order_created_at", StringType())
    ])
    return spark_session.createDataFrame(data, schema)


def get_order_creation_df(spark_session):
    """
+--------------------+----------+-----------+---------+---------------+---------------+
|            order_id|order_year|order_month|order_day|order_dayofweek|order_dayofyear|
+--------------------+----------+-----------+---------+---------------+---------------+
|8deafc7f-60df-423...|      2019|          1|       21|              2|             21|
|8f8f3633-0e80-48a...|      2019|          1|       31|              5|             31|
|17c91ae3-1f5e-4a7...|      2019|          1|        8|              3|              8|
|5b8670c0-e2f1-4a6...|      2019|          1|       31|              5|             31|
|71abcdd3-fa2f-4d7...|      2019|          1|       13|              1|             13|
+--------------------+----------+-----------+---------+---------------+---------------+
    """
    data = [
        Row(order_id='8deafc7f-60df-4235-9629-db5f9ec82458',
            order_year=2019,
            order_month=1,
            order_day=21,
            order_dayofweek=2,
            order_dayofyear=21),
        Row(order_id='8f8f3633-0e80-48ae-91a4-2161d9fdda24',
            order_year=2019,
            order_month=1,
            order_day=31,
            order_dayofweek=5,
            order_dayofyear=31),
        Row(order_id='17c91ae3-1f5e-4a70-8efb-08cf3f8498c4',
            order_year=2019,
            order_month=1,
            order_day=8,
            order_dayofweek=3,
            order_dayofyear=8),
        Row(order_id='5b8670c0-e2f1-4a66-bc16-553d45dfc848',
            order_year=2019,
            order_month=1,
            order_day=31,
            order_dayofweek=5,
            order_dayofyear=31),
        Row(order_id='71abcdd3-fa2f-4d75-b5ee-68aa262bfe58',
            order_year=2019,
            order_month=1,
            order_day=13,
            order_dayofweek=1,
            order_dayofyear=13)
    ]
    schema = StructType([
        StructField("order_id", StringType()),
        StructField("order_year", IntegerType()),
        StructField("order_month", IntegerType()),
        StructField("order_day", IntegerType()),
        StructField("order_dayofweek", IntegerType()),
        StructField("order_dayofyear", IntegerType())
    ])
    return spark_session.createDataFrame(data, schema)


def test_order_creation(spark_session):
    order_df = get_order_df(spark_session)
    features_df = OrderCreation().transform(order_df)
    expected_df = get_order_creation_df(spark_session)

    assert features_df.count() == 5
    assert are_dfs_equal(features_df, expected_df)
