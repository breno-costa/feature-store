# Transformations

This module provides an extensible framework for creating transformation jobs that can be used to create feature engineering functions and similar ones.

## How it works

This module uses structured streaming available on the Spark.

When the application is started, the catalog of transformations is used to create the structured streaming spark jobs. Each transformation generates a spark job running on the cluster with a shared spark session.

The proposed approach has some advantages:

* Horizontal scalability for multiple workers.
* Creation of streaming jobs using dataframes api.
* Batch and streaming transformations jobs using the same code!

## Writing a new transformation

The following example shows how to use the order entity as input to create features related to the order creation date.

### Transformation class

The first step is creating a new transformation class. See the [order creation example](./transformations/definitions/order_creation.py):

```python
@dataclass
class OrderCreationDate(FeatureGroup):
    name: str = "order_creation_date"
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
                f.dayofmonth("order_created_at").alias("order_day")
            )
        )
```

The class attributes:

* name: feature group name, must be unique on the feature store.
* key: output field to be used as primary key. It's also used as kafka key.
* input_entity: entity name to be used as input. This name is used to subscribe to the kafka topic.
* output_entity: entity name to be used as output. It composes the redis table name.

The method transform:

* That method receives a input dataframe (code works for any spark dataframe), and returns the transformed dataframe.

This class can be used to run batch transformation jobs with no modification.

### Unit Tests

Once the transformation class is finished, you just need to write the unit tests mocking input data and expected output data for that function. The previous example receives an order dataframe as input, so you just need to create a mocked dataframe:

```python
def get_order_df(spark_session):
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
```

After that, you need to create the expected dataframe after applying transformation.

```python
def get_order_creation_df(spark_session):
    data = [
        Row(order_id='8deafc7f-60df-4235-9629-db5f9ec82458',
            order_year=2019,
            order_month=1,
            order_day=21),
        Row(order_id='8f8f3633-0e80-48ae-91a4-2161d9fdda24',
            order_year=2019,
            order_month=1,
            order_day=31),
        Row(order_id='17c91ae3-1f5e-4a70-8efb-08cf3f8498c4',
            order_year=2019,
            order_month=1,
            order_day=8),
        Row(order_id='5b8670c0-e2f1-4a66-bc16-553d45dfc848',
            order_year=2019,
            order_month=1,
            order_day=31),
        Row(order_id='71abcdd3-fa2f-4d75-b5ee-68aa262bfe58',
            order_year=2019,
            order_month=1,
            order_day=13)
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
```

And create the unit tests to make the assertions:

```python
def test_order_creation(spark_session):
    order_df = get_order_df(spark_session)
    features_df = OrderCreation().transform(order_df)
    expected_df = get_order_creation_df(spark_session)

    assert features_df.count() == 5
    assert are_dfs_equal(features_df, expected_df)
```

This is a very important step to guarantee the quality of the feature engineering jobs in terms of software engineering.

### Catalog

Lastly the transformation class must be registered to run properly as transformation jobs. You just need to add it on the [definition catalog](./transformations/catalog.py).

## Useful commands

To run linters (mypy, flake8, bandit):

```bash
make lint
```

To build the project:

```bash
make build
```

To run tests:

```bash
make check
```

To start transformation jobs and related services:

```bash
make start
```
