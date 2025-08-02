import os
import json
import time
from common.utils import create_kafka_producer, get_logger

TOPIC = "events"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVENT_FILE = os.path.join(BASE_DIR, "sample_events.json")

logger = get_logger("IngestService")

if __name__ == "__main__":
    producer = create_kafka_producer()

    with open(EVENT_FILE) as f:
        events = json.load(f)

    logger.info("🚀 Sending events to Kafka...")
    for event in events:
        producer.send(TOPIC, value=event)
        logger.info(f"✅ Sent: {event}")
        time.sleep(1)

    producer.flush()
    logger.info("🎯 All events sent!")
