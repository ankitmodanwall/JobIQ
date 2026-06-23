import json
import logging
import os

logger = logging.getLogger(__name__)

# ✅ Kafka disabled by default to avoid connection issues
producer = None

def send_resume_event(resume_data):
    """Send resume event to Kafka (disabled)"""
    logger.info(f"ℹ️ Kafka disabled. Would send: {json.dumps(resume_data)}")
    return {"status": "disabled", "message": "Kafka events disabled"}

# ✅ Uncomment below to enable Kafka when available
# try:
#     from kafka import KafkaProducer
#     producer = KafkaProducer(
#         bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
#         value_serializer=lambda v: json.dumps(v).encode('utf-8')
#     )
#     logger.info("✅ Kafka producer initialized")
# except Exception as e:
#     logger.warning(f"⚠️ Kafka not available: {e}")
#     producer = None