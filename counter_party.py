# counter_party.py
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=3,
)

def send_confirmation(text):
    msg = {"type": "Counter_party", "text": text}
    meta = producer.send("Counter_party", value=msg).get(timeout=10)
    print(f"Sent Counter_party confirmation; topic {meta.topic} offset {meta.offset}")

if __name__ == "__main__":
    print("Counter party producer. Type CONFIRM to send confirmation.")
    try:
        while True:
            txt = input("> ").strip()
            if not txt:
                continue
            if txt.lower() in ("exit","quit"):
                break
            send_confirmation(txt)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()
        producer.close()
