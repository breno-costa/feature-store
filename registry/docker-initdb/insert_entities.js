
db = db.getSiblingDB('registry')

db.schema.insert(
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
)

db.schema.insert(
    {
        "subject": "entity-order",
        "type": "entity",
        "name": "order",
        "key": "order_id",
        "properties": {
            "type": "struct",
            "fields": [
                {
                    "metadata": {},
                    "name": "cpf",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "customer_id",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "customer_name",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "delivery_address_city",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "delivery_address_country",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "delivery_address_district",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "delivery_address_external_id",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "delivery_address_latitude",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "delivery_address_longitude",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "delivery_address_state",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "delivery_address_zip_code",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "items",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "merchant_id",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "merchant_latitude",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "merchant_longitude",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "merchant_timezone",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "order_created_at",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "order_id",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "order_scheduled",
                    "nullable": true,
                    "type": "boolean"
                },
                {
                    "metadata": {},
                    "name": "order_scheduled_date",
                    "nullable": true,
                    "type": "string"
                },
                {
                    "metadata": {},
                    "name": "order_total_amount",
                    "nullable": true,
                    "type": "double"
                },
                {
                    "metadata": {},
                    "name": "origin_platform",
                    "nullable": true,
                    "type": "string"
                }
            ]
        }
    }
)
