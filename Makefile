start:
	docker-compose up --build -d

stop:
	docker-compose stop

purge:
	docker-compose down -v

logs:
	docker-compose logs -f


### KAFKA ###
start-kafka:
	docker-compose up -d kafka kafdrop

logs-kafka:
	docker-compose logs -f kafka


### REDIS
start-redis:
	docker-compose up -d redis

logs-redis:
	docker-compose logs -f redis


### TRANFORMATIONS ###
start-transformations:
	docker-compose up --build -d transformations

stop-transformations:
	docker-compose stop transformations

logs-transformations:
	docker-compose logs -f transformations


### SINKS ###
start-sinks:
	docker-compose up --build -d sinks

stop-sinks:
	docker-compose stop sinks

logs-sinks:
	docker-compose logs -f sinks


### PRODUCERS ###
build-producer:
	docker build -f producer/Dockerfile -t producer:latest producer

produce-orders: build-producer
	docker run -v $(PWD)/data:/app/data --network=host producer:latest producer \
		--filepath data/orders_100k.json.gz \
		--filetype json \
		--entity order \
		--entity_key order_id \
		--timestamp_field order_created_at

produce-status: build-producer
	docker run -v $(PWD)/data:/app/data --network=host producer:latest producer \
		--filepath data/status_100k.json.gz \
		--filetype json \
		--entity status \
		--entity_key status_id \
		--timestamp_field created_at
