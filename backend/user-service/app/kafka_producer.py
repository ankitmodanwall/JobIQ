import json
import logging

logger = logging.getLogger(__name__)

# ✅ Kafka disabled - no connection attempts
def send_user_event(user_data):
    """Send user event to Kafka (disabled for now)"""
    logger.info(f"ℹ️ Kafka disabled. Would send: {json.dumps(user_data)}")
    # ✅ Fake success - no actual Kafka connection
    return {"status": "disabled", "message": "Kafka events disabled"}

# Uncomment below to enable Kafka when available
# try:
#     from kafka import KafkaProducer
#     import os
#     
#     producer = KafkaProducer(
#         bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
#         value_serializer=lambda v: json.dumps(v).encode('utf-8')
#     )
#     logger.info("✅ Kafka producer initialized")
# except Exception as e:
#     logger.warning(f"⚠️ Kafka not available: {e}")
#     producer = None