# nse_exchange_consumer.py
from kafka import KafkaConsumer
import json, time
import nse_exchange_producer as producer_helpers

consumer = KafkaConsumer(
    "Trade_Order", "Counter_party",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="nse-exchange-group",
    value_deserializer=lambda b: json.loads(b.decode("utf-8"))
)

# very simple in-memory pending order storage
pending_order = None

def process_trade_order(msg):
    global pending_order
    # msg example: {"type":"Trade_Order","qty":100,"symbol":"SBI","price":985}
    qty = int(msg.get("qty"))
    symbol = msg.get("symbol")
    price = float(msg.get("price"))
    pending_order = {"qty": qty, "symbol": symbol, "price": price}
    print(f"[NSE-Consumer] Received Trade_Order: {qty} {symbol} @ {price}")
    # For demo: we can process immediately OR wait for counter-party confirmation.
    # Here we'll wait for a confirmation to produce the outputs. But to demo both ways,
    # we can also automatically process immediately if desired. Uncomment if you want immediate:
    # produce_outputs_for_pending_order()

def process_counter_party(msg):
    # msg example: {"type":"Counter_party","text":"CONFIRM"}
    global pending_order
    print(f"[NSE-Consumer] Received Counter_party message: {msg.get('text')}")
    # If confirmation and pending order exists -> produce outputs
    if pending_order is not None:
        produce_outputs_for_pending_order()
    else:
        print("[NSE-Consumer] No pending order to match confirmation.")

def produce_outputs_for_pending_order():
    global pending_order
    if not pending_order:
        return
    qty = pending_order["qty"]
    symbol = pending_order["symbol"]
    price = pending_order["price"]
    total_amount = qty * price
    # produce demat and cash messages via producer helper functions
    producer_helpers.produce_demat(symbol, qty)
    producer_helpers.produce_cash_movement(total_amount)
    print(f"[NSE-Consumer] Produced DEMAT {qty} and DEBIT {int(total_amount)} to topics.")
    # clear pending after processing
    pending_order = None

def main_loop():
    print("[NSE-Consumer] Starting consumer... Listening to Trade_Order and Counter_party topics.")
    try:
        for msg in consumer:
            try:
                payload = msg.value
            except Exception as e:
                print("Failed to decode message:", e)
                continue
            if not isinstance(payload, dict):
                print("Unexpected message:", payload)
                continue
            mtype = payload.get("type")
            if mtype == "Trade_Order":
                process_trade_order(payload)
            elif mtype == "Counter_party":
                process_counter_party(payload)
            else:
                print("[NSE-Consumer] Unknown message type:", mtype)
    except KeyboardInterrupt:
        print("Stopping NSE consumer...")
    finally:
        consumer.close()
        producer_helpers.flush_and_close()

if __name__ == "__main__":
    main_loop()
