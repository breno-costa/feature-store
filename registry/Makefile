SHELL := /bin/bash
PACKAGE_NAME = registry

DOCKER_IMG := $(PACKAGE_NAME):latest
DOCKER_RUN := docker run --rm

MOUNT_TESTS := -v $(PWD)/tests/unit:/app/tests/unit
MOUNT_SOURCE := -v $(PWD)/$(PACKAGE_NAME):/app/$(PACKAGE_NAME)

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Missing '$*' variable"; \
		exit 1; \
	fi

clean:
	docker volume rm $(PACKAGE_NAME) --force
	docker rmi $(DOCKER_IMG) --force

build:
	docker build -t $(DOCKER_IMG) .

shell: build
	$(DOCKER_RUN) -it $(DOCKER_IMG) bash


mypy:
	$(DOCKER_RUN) $(MOUNT_TESTS) $(MOUNT_SOURCE) -w /app brenocosta0901/mypy:latest $(PACKAGE_NAME) tests

flake8:
	$(DOCKER_RUN) $(MOUNT_TESTS) $(MOUNT_SOURCE) -w /app brenocosta0901/flake8:latest $(PACKAGE_NAME) tests

bandit:
	$(DOCKER_RUN) $(MOUNT_TESTS) $(MOUNT_SOURCE) -w /app brenocosta0901/bandit:latest -r $(PACKAGE_NAME)

lint: mypy flake8 bandit


check: build
	docker-compose up -d
	$(DOCKER_RUN) --network=host $(MOUNT_TESTS) $(DOCKER_IMG) python -B -m pytest -p no:cacheprovider --cov=$(PACKAGE_NAME)
	docker-compose down

run:
	docker-compose up --build

start:
	docker-compose up --build -d

stop:
	docker-compose stop

purge:
	docker-compose down -v

logs:
	docker-compose logs -f
