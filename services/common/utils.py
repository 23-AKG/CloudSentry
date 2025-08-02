import json
import time
import logging
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable

BOOTSTRAP_SERVERS = "kafka:9092"

def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    return logging.getLogger(name)


def create_kafka_producer(retries=5, delay=5):
    logger = get_logger("KafkaProducer")
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"[Attempt {attempt}] Connecting KafkaProducer to {BOOTSTRAP_SERVERS}...")
            producer = KafkaProducer(
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            logger.info("✅ KafkaProducer connected")
            return producer
        except NoBrokersAvailable:
            logger.warning(f"⚠️ Kafka not available, retrying in {delay}s...")
            time.sleep(delay)
    raise RuntimeError("❌ Could not connect KafkaProducer after retries.")


def create_kafka_consumer(topic, group_id, retries=5, delay=5):
    logger = get_logger("KafkaConsumer")
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"[Attempt {attempt}] Connecting KafkaConsumer to {BOOTSTRAP_SERVERS}...")
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id=group_id
            )
            logger.info("✅ KafkaConsumer connected")
            return consumer
        except NoBrokersAvailable:
            logger.warning(f"⚠️ Kafka not available, retrying in {delay}s...")
            time.sleep(delay)
    raise RuntimeError("❌ Could not connect KafkaConsumer after retries.")
