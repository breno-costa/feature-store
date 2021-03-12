import requests
import json


BASE_URL = "http://localhost:8000"


def test_get_schema():
    resp = requests.get(f"{BASE_URL}/schemas")
    schemas = resp.json()
    assert len(schemas) == 2


def test_get_schema():
    resp = requests.get(f"{BASE_URL}/schemas/entity-status")
    entity = resp.json()
    assert resp.status_code == 200
    assert entity["subject"] == "entity-status"
    assert entity["type"] == "entity"
    assert entity["name"] == "status"
    assert entity["key"] == "status_id"


def test_post_schema():
    payload = {
        "subject": "type-name",
        "type": "type",
        "name": "name",
        "key": "key",
        "properties": {}
    }
    resp = requests.post(f"{BASE_URL}/schemas", json.dumps(payload))
    assert resp.status_code == 200

    # Check number of schemas
    resp = requests.get(f"{BASE_URL}/schemas")
    schemas = resp.json()
    assert len(schemas) == 3

    # Check if get is working
    resp = requests.get(f"{BASE_URL}/schemas/type-name")
    entity = resp.json()
    assert resp.status_code == 200
    assert entity["subject"] == "type-name"
    assert entity["type"] == "type"
    assert entity["name"] == "name"
    assert entity["key"] == "key"
    