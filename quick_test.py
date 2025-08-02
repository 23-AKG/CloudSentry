import time
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer, KafkaConsumer
import json
import logging

BROKER = "localhost:9092"
EVENT_TOPIC = "events"
ALERT_TOPIC = "alerts"
TEST_GROUP = "quicktest-group"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def reset_topics():
    admin = KafkaAdminClient(bootstrap_servers=BROKER, client_id="quicktest-admin")

    # Delete topics if they exist
    try:
        admin.delete_topics([EVENT_TOPIC, ALERT_TOPIC])
        logging.info("🧹 Deleted old topics: events, alerts")
        time.sleep(3)  # give Kafka some time to clean
    except Exception as e:
        logging.warning(f"Topics might not exist yet: {e}")

    # Create topics fresh
    topics = [
        NewTopic(EVENT_TOPIC, num_partitions=1, replication_factor=1),
        NewTopic(ALERT_TOPIC, num_partitions=1, replication_factor=1)
    ]
    try:
        admin.create_topics(new_topics=topics)
        logging.info("✨ Created fresh topics: events, alerts")
    except Exception as e:
        logging.warning(f"Topics might already exist: {e}")

    admin.close()


def quick_test():
    # Step 1: Cleanup topics
    reset_topics()

    # Step 2: Create Producer
    producer = KafkaProducer(
        bootstrap_servers=BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    logging.info("🚀 Kafka Producer ready")

    # Step 3: Produce a test event
    test_event = {"timestamp": "2025-08-02T10:00:00", "ip": "192.168.0.50", "event": "failed_login"}
    producer.send(EVENT_TOPIC, value=test_event)
    logging.info(f"✅ Sent test event: {test_event}")
    producer.flush()

    # Step 4: Create Consumer for Alerts
    consumer = KafkaConsumer(
        ALERT_TOPIC,
        bootstrap_servers=BROKER,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id=TEST_GROUP
    )
    logging.info("👂 Listening for alerts... (15s max)")

    start_time = time.time()
    alert_received = False
    for msg in consumer:
        logging.warning(f"🚨 ALERT RECEIVED: {msg.value}")
        alert_received = True
        break
        if time.time() - start_time > 15:
            break

    if not alert_received:
        logging.info("⚠️ No alert received within 15s")

    # Step 5: Cleanup
    producer.close()
    consumer.close()
    logging.info("🧼 Test complete — producer & consumer closed")


if __name__ == "__main__":
    quick_test()
