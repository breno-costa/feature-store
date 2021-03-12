FROM python:3.8-slim

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

# Docker install requirements only if requirements.txt has changed
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Docker install package dependencies again only if setup.py has changed
COPY ./setup.py ./
RUN pip install .

# Docker install package with no dependencies in every build (trick to reduce time in the Gitlab CI)
COPY ./registry ./registry
COPY ./tests ./tests
RUN pip install . --no-deps
