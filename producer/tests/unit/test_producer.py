from _io import TextIOWrapper
from tempfile import NamedTemporaryFile
from gzip import GzipFile

from kafka.future import Future

from producer import file_producer


def test_open_file():
    temp_file = NamedTemporaryFile(mode='r', suffix='.json')
    f = file_producer.open_file(temp_file.name)
    assert isinstance(f, TextIOWrapper)


def test_open_gzip_file():
    temp_file = NamedTemporaryFile(mode='r', suffix='.json.gz')
    f = file_producer.open_file(temp_file.name)
    assert isinstance(f, GzipFile)


def test_get_record():
    record = file_producer.get_record(
        line='{"id": 1, "value": 10}',
        filetype="json"
    )
    assert record == {"id": 1, "value": 10}


def test_get_record_when_json_is_bad_formatted():
    record = file_producer.get_record(
        line='{"id": 1, "value": 10',
        filetype="json"
    )
    assert record is None


def test_get_key():
    record = {
        "id": 1,
        "value": 10
    }
    key = file_producer.get_key(record=record, entity_key="id")
    assert key == 1


def test_get_key_when_key_field_is_none():
    record = {
        "id": 1,
        "value": 10
    }
    key = file_producer.get_key(record=record)
    assert key is None


def test_get_timestamp_ms():
    record = {
        "id": 1,
        "date": "2019-01-17T22:50:06.000Z"
    }
    timestamp_ms = file_producer.get_timestamp_ms(
        record=record,
        timestamp_field="date",
        timestamp_format="%Y-%m-%dT%H:%M:%S.000Z"
    )
    assert timestamp_ms == 1547765406


def test_get_timestamp_ms_when_timestamp_field_is_none():
    record = {
        "id": 1
    }
    timestamp_ms = file_producer.get_timestamp_ms(record=record)
    assert timestamp_ms is None


def test_get_topic_name():
    assert file_producer.get_topic_name("company") == "entity-company"


class MockedKafkaProducer:
    def __init__(self, *args, **xargs):
        pass

    def send(self, *args, **xargs):
        return Future().success(value="any")


def test_run(monkeypatch):
    monkeypatch.setattr(file_producer, "KafkaProducer", MockedKafkaProducer)

    data = """{"cpf": "79719037778", "order_id": "6ee39c63-7963-4002-b84a-e2ad6f94ac8f", "order_created_at": "2019-01-17T22:49:28.000Z"}
{"cpf": "80532101763", "order_id": "dd4f8f0a-c2cb-45c6-a002-c3be6b305e5f", "order_created_at": "2019-01-17T22:50:06.000Z"}"""

    with NamedTemporaryFile(mode='w', suffix='.json') as f:
        f.write(data)
        f.flush()

        record_count = file_producer.run(
            filepath=f.name,
            filetype="json",
            entity_key="order_id",
            timestamp_field="order_created_at",
            timestamp_format="%Y-%m-%dT%H:%M:%S.000Z",
            entity="orders"
        )

        assert record_count == 2


def test_run_with_limit(monkeypatch):
    monkeypatch.setattr(file_producer, "KafkaProducer", MockedKafkaProducer)

    data = """{"cpf": "79719037778", "order_id": "6ee39c63-7963-4002-b84a-e2ad6f94ac8f", "order_created_at": "2019-01-17T22:49:28.000Z"}
{"cpf": "80532101763", "order_id": "dd4f8f0a-c2cb-45c6-a002-c3be6b305e5f", "order_created_at": "2019-01-17T22:50:06.000Z"}"""

    with NamedTemporaryFile(mode='w', suffix='.json') as f:
        f.write(data)
        f.flush()

        record_count = file_producer.run(
            filepath=f.name,
            filetype="json",
            entity_key="order_id",
            timestamp_field="order_created_at",
            timestamp_format="%Y-%m-%dT%H:%M:%S.000Z",
            entity="orders",
            limit=1
        )

        assert record_count == 1
