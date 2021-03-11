from transformations import settings


def test_settings():
    assert settings.KAFKA_BROKER == "localhost:9092"
