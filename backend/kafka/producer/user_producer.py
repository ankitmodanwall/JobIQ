from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data = {
    "user_id": 1,
    "name": "Ankit",
    "email": "ankit@test.com"
}

producer.send("users", data)
producer.flush()

print("Message Sent Successfully")