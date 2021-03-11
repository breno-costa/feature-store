from tempfile import NamedTemporaryFile

from transformations.registry import schemas


def test_get_filename():
    expected = "/app/transformations/registry/entity-status.json"
    assert schemas.get_filename("entity-status") == expected


def test_get_schema(monkeypatch):
    schema_example = """
    {
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
            }
        ]
    }
    """
    with NamedTemporaryFile(mode="w", suffix=".json") as f:
        f.write(schema_example)
        f.flush()

        monkeypatch.setattr(schemas, "get_filename", lambda s: f.name)
        schema = schemas.get_schema(full_schema_name="event-status")

        assert schema == {
            "type": "struct",
            "fields": [
                {
                    "name": "status_id",
                    "type": "string",
                    "nullable": True,
                    "metadata": {}
                },
                {
                    "name": "created_at",
                    "type": "string",
                    "nullable": True,
                    "metadata": {}
                }
            ]
        }


def test_get_full_schema_name():
    full_schema_name = schemas.get_full_schema_name("entity", "order")
    assert full_schema_name == "entity-order"


def test_get_entity_name():
    full_entity_name = schemas.get_entity_name("order")
    assert full_entity_name == "entity-order"


def test_get_featuregroup_name():
    full_feature_name = schemas.get_featuregroup_name("customer_orders")
    assert full_feature_name == "featuregroup-customer_orders"
