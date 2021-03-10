# Producer

Python application emulating the production of entities into the kafka.

The approach proposed here is reading a input file line by line and sending the records to the kafka broker. The motivation behind this idea is to emulate a microservice producing events according to the user interactions.

This project relies heavily on the kafka. You must to have kafka broker running before to produce data properly. A kafka broker instance can be started using docker-compose available on the repository.

## Getting started

### Pip

You can install python package and run it using the command line.

```bash
pip install .
```

Follows an order producer example below.

```bash
producer --filepath data/order.json.gz \
	 --filetype json \
	 --entity order \
	 --entity_key order_id \
	 --timestamp_field order_created_at
```

### Docker

Alternatively you can build the image and run as a docker container.

```bash
make build
```

Follows the order producer

```bash
docker run -v $(pwd)/data:/app/data --network=host producer:latest producer \
		--filepath data/order.json.gz \
		--filetype json \
		--entity order \
		--entity_key order_id \
		--timestamp_field order_created_at
```

PS: Mount docker volume as a folder where your input file is located.

## Parameters

Follows a list of parameters that can be used:

| Parameter          | Description                                                                       |
|--------------------|-----------------------------------------------------------------------------------|
| --filepath         | Filepath to be sent to the kafka                                                  |
| --filetype         | File type (json, csv)                                                             |
| --entity           | Entity name                                                                       |
| --entity_key       | Field name used as kafka key                                                      |
| --timestamp_field  | Optional. Field name used as kafka timestamp (default: None)                      |
| --timestamp_format | Optional. Format to convert timestamp fields (default: `%Y-%m-%dT%H:%M:%S.000Z)`) |
| --limit            | Optional. Maximum number of records sent to kafka (default: None)                 |


## Useful commands

To run linters (mypy, flake8, bandit):

```bash
make lint
```

To run tests:

```bash
make check
```
