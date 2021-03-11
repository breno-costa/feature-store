# Feature Store

Feature Store


## Schema Registry

The schema registry is responsible to store schema files,
and provides a query layer for the applications. Each producer
must register a schema before sending the data to Kafka.

There are two fundamental concepts used by the schema registry
when a schema is created.

* Schema type: related to the data lifecycle (entity, feature-group)
* Schema name: meaningful name that defines the data (order, status, order-by-user)

The full schema name is built with both parts concatenated as
the examples listed below.

* entity-order
* entity-status
* entity-customer
* entity-restaurant
* featuregroup-customer-orders

The kafka topics are created with the full schema names.
