# hdfc_broker_producer.py
from kafka import KafkaProducer
import json
import sys

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=3,
)

def send_trade_order(qty, symbol, price):
    msg = {"type": "Trade_Order", "qty": int(qty), "symbol": symbol, "price": float(price)}
    future = producer.send("Trade_Order", value=msg)
    meta = future.get(timeout=10)
    print(f"Sent Trade_Order -> topic {meta.topic} partition {meta.partition} offset {meta.offset}")

if __name__ == "__main__":
    print("HDFC Broker Producer. Enter trade in format: qty,symbol,price")
    try:
        while True:
            line = input("> ").strip()
            if not line:
                continue
            if line.lower() in ("exit","quit"):
                break
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                print("Bad format. Use: qty,symbol,price")
                continue
            send_trade_order(parts[0], parts[1], parts[2])
    except KeyboardInterrupt:
        print("Exiting producer.")
    finally:
        producer.flush()
        producer.close()
