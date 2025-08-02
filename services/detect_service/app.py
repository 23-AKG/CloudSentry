from common.utils import create_kafka_consumer, create_kafka_producer, get_logger
from rules import check_brute_force

EVENT_TOPIC = "events"
ALERT_TOPIC = "alerts"

logger = get_logger("DetectService")

if __name__ == "__main__":
    consumer = create_kafka_consumer(EVENT_TOPIC, group_id="detection-group")
    producer = create_kafka_producer()

    logger.info("👁️‍🗨️ Detect Service is watching...")

    for msg in consumer:
        event = msg.value
        alert = check_brute_force(event)
        if alert:
            producer.send(ALERT_TOPIC, value=alert)
            logger.warning(f"🚨 Alert Generated: {alert}")
