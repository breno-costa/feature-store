# Registry

> Disclaimer: this module is running properly, but it's not yet integrated with other system modules. I have written TODO items on the producer, transformations and sink modules.

The schema registry is responsible to store schema files, and provides a query layer for the applications. Each producer must register a schema before sending the data to Kafka.

## Naming Convention

There are two fundamental concepts used by the schema registry when a schema is created.

* Schema type: related to the data lifecycle (entity, feature-group)
* Schema name: meaningful name that defines the data (order, status, order-by-user)

The schema subject is built with both parts concatenated as the examples below.

* entity-order
* entity-status
* featuregroup-customer-orders

The kafka topic names are the schema subjects.


## API

Please checkout the [OpenAPI documentation](http://localhost:8000/docs) to see the available endpoints. The registry API has operations to handle schemas on the database. An example on how to use schema registry is shown below to get schema by subject.

```bash
$ curl http://localhost:8000/schemas/order-status
{
    "subject": "entity-status",
    "type": "entity",
    "name": "status",
    "key": "status_id",
    "properties": {
        "type": "struct",
        "fields": [
            {
                "name": "status_id",
                "type": "string",
                "nullable": true,
                "metadata": {}
            },
            {
                "name": "created_at",
                "type": "string",
                "nullable": true,
                "metadata": {}
            },
            {
                "name": "order_id",
                "type": "string",
                "nullable": true,
                "metadata": {}
            },
            {
                "name": "value",
                "type": "string",
                "nullable": true,
                "metadata": {}
            }
        ]
    }
}
```
