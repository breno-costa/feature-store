FROM brenocosta0901/spark-py:3.0.1

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && \
    apt-get install -y --no-install-recommends git vim && \
    rm -rf /var/lib/apt/lists/*

# Cache Spark packages described above.
ENV APP_PACKAGES="--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,com.redislabs:spark-redis_2.12:2.6.0"
ENV PYSPARK_SUBMIT_ARGS="$APP_PACKAGES pyspark-shell"
RUN spark-submit run-example $APP_PACKAGES example-class | true

# Docker install requirements only if requirements.txt has changed
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Docker install package dependencies again only if setup.py has changed
COPY ./setup.py ./
RUN pip install .

# Docker install package with no dependencies in every build (trick to reduce time in the Gitlab CI)
COPY ./sinks ./sinks
COPY ./tests ./tests
RUN pip install . --no-deps
