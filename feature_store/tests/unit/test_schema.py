from tempfile import NamedTemporaryFile

from feature_store.schemas import schemas


def test_get_filename():
    expected = "/app/feature_store/schemas/event-status.json"
    assert schemas.get_filename("event-status") == expected


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
        schema = schemas.get_schema(schema_name="event-status")

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
