# nse_exchange_producer.py
from kafka import KafkaProducer
import json, time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=3,
)

def produce_demat(symbol, qty):
    msg = {"type": "Demat_allocation", "action": "DEMAT", "symbol": symbol, "qty": int(qty)}
    m = producer.send("Demat_allocation", value=msg).get(timeout=10)
    print(f"[NSE-Producer] Produced Demat -> offset {m.offset}")

def produce_cash_movement(amount):
    msg = {"type": "Cash_movement", "action": "DEBIT", "amount": float(amount)}
    m = producer.send("Cash_movement", value=msg).get(timeout=10)
    print(f"[NSE-Producer] Produced Cash movement -> offset {m.offset}")

def flush_and_close():
    producer.flush()
    producer.close()
