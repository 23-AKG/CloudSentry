from common.utils import create_kafka_consumer, get_logger

ALERT_TOPIC = "alerts"

logger = get_logger("AlertService")

if __name__ == "__main__":
    consumer = create_kafka_consumer(ALERT_TOPIC, group_id="alert-group")

    logger.info("📢 Alert Service is listening for alerts...\n")

    for msg in consumer:
        alert = msg.value
        logger.warning(f"🚨 ALERT: {alert}")
