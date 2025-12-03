# hdfc_broker_consumer.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "Demat_allocation", "Cash_movement",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="hdfc-broker-group",
    value_deserializer=lambda b: json.loads(b.decode("utf-8"))
)

print("[HDFC-Consumer] Listening for Demat_allocation and Cash_movement topics...")
try:
    for msg in consumer:
        payload = msg.value
        if not isinstance(payload, dict):
            print("Non-json message:", payload)
            continue
        t = payload.get("type")
        if t == "Demat_allocation" or payload.get("action") == "DEMAT":
            print("[HDFC-Consumer] DEMAT received:", payload)
        elif t == "Cash_movement" or payload.get("action") == "DEBIT":
            print("[HDFC-Consumer] CASH movement received:", payload)
        else:
            print("[HDFC-Consumer] Unknown message:", payload)
except KeyboardInterrupt:
    print("Stopping HDFC consumer.")
finally:
    consumer.close()
