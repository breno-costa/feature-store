import os


SPARK_UI_PORT = os.getenv("SPARK_UI_PORT", "4050")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
