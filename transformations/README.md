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

The first step is creating a new transformation class:

```python
from dataclasses import dataclass
from pyspark.sql import DataFrame
from pyspark.sql import functions as f
from transformations.core import FeatureGroup


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

Once the transformation class is finished, you just need to write the unit tests mocking input data and expected output data for that function.

This is a very important step to guarantee the quality of the feature engineering jobs in terms of software engineering.

### Catalog

Lastly the transformation class must be registered to run properly as transformation jobs. You just need to add it on the definition catalog.


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
