SHELL := /bin/bash
PACKAGE_NAME = sinks

DOCKER_IMG := $(PACKAGE_NAME):latest
DOCKER_RUN := docker run --rm -v $(PWD)/tests:/app/tests

MOUNT_TESTS := -v $(PWD)/tests:/app/tests
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


check: build
	$(DOCKER_RUN) $(MOUNT_TESTS) $(DOCKER_IMG) python -B -m pytest -p no:cacheprovider --cov=$(PACKAGE_NAME)

check/%: build
	$(DOCKER_RUN) $(MOUNT_TESTS) $(DOCKER_IMG) python -B -m pytest -p no:cacheprovider $@


mypy:
	$(DOCKER_RUN) $(MOUNT_TESTS) $(MOUNT_SOURCE) -w /app brenocosta0901/mypy:latest $(PACKAGE_NAME) tests

flake8:
	$(DOCKER_RUN) $(MOUNT_TESTS) $(MOUNT_SOURCE) -w /app brenocosta0901/flake8:latest $(PACKAGE_NAME) tests

bandit:
	$(DOCKER_RUN) $(MOUNT_TESTS) $(MOUNT_SOURCE) -w /app brenocosta0901/bandit:latest -r $(PACKAGE_NAME)

lint: mypy flake8 bandit
