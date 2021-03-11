# Sinks

This module is responsible to run sink jobs and allows you to export data from Apache Kafka topics to engines. 


## How it works

This module uses structured streaming available on the Spark.

When the application is started, the catalog of sinks is used to create the structured streaming spark jobs. Each sink generates a spark job running on the cluster with a shared spark session.

There are two sinks available for general use.

* Redis: in-memory database used as feature store online storage.
* Console: used for debug purposes.


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
