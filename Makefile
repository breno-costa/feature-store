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
	@docker build -f producer/Dockerfile producer

produce-orders: build-producer
	@bash download_files.sh \
		https://ifood-data-architect-test-source.s3-sa-east-1.amazonaws.com/order.json.gz \
		data/order.json.gz

	@docker run -v $(PWD)/data:/app/data --network=host producer:latest producer \
		--filepath data/order.json.gz \
		--filetype json \
		--entity order \
		--entity_key order_id \
		--timestamp_field order_created_at

produce-status: build-producer
	@bash download_files.sh \
		https://ifood-data-architect-test-source.s3-sa-east-1.amazonaws.com/status.json.gz \
		data/status.json.gz

	@docker run -v $(PWD)/data:/app/data --network=host producer:latest producer \
		--filepath data/status.json.gz \
		--filetype json \
		--entity status \
		--entity_key status_id \
		--timestamp_field created_at
