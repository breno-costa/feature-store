

def test_get_mongo_uri(monkeypatch):
    monkeypatch.setenv("MONGO_USER", "admin")
    monkeypatch.setenv("MONGO_PASSWORD", "secret")
    monkeypatch.setenv("MONGO_DATABASE", "registry")
    monkeypatch.setenv("MONGO_HOST", "mongo")
    monkeypatch.setenv("MONGO_PORT", "27017")

    from registry.settings import get_mongo_uri

    expected = "mongodb://admin:secret@mongo:27017/registry"
    assert get_mongo_uri() == expected
