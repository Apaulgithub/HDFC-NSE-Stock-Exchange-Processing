# Real-Time Trade Processing System using Apache Kafka

![Flowchart](https://github.com/user-attachments/assets/dc10f7d4-82cf-48e2-a6a1-e0f891a6ebf7)

<sub>Flowchart: Real-time processing pipeline between HDFC Broker, NSE Exchange, and Counter-party, built using Apache Kafka.</sub>

---

Click below to explore the core scripts used in this real-time Kafka event-driven system:

- `hdfc_broker_producer.py`  
- `hdfc_broker_consumer.py`  
- `nse_exchange_producer.py`  
- `nse_exchange_consumer.py`  
- `counter_party.py`

---

## Problem Statement

Modern financial trading systems require **high-speed, fault-tolerant, real-time data pipelines** to process orders, confirmations, settlements, demat allocation, and cash movements.

This project simulates a **real-time stock trade lifecycle** using Apache Kafka, involving three actors:

- **HDFC Broker** – submits customer trade orders  
- **NSE Exchange** – processes trade and settlement  
- **Counter-party system** – sends confirmation messages  

Each actor produces or consumes Kafka events through dedicated micro-scripts, closely resembling real trading operations.

---

## Project Summary

This project implements a **Kafka-based event-streaming architecture** to simulate a full trade workflow.

### Stage 1 — HDFC Broker places an order  
A user enters a trade request (e.g., **100 shares of SBI at ₹985**).  
`hdfc_broker_producer.py` publishes this to the **Trade_Order** Kafka topic.

---

### Stage 2 — Counter-party Confirmation  
A confirmation message (**CONFIRM**) is produced to the **Counter_party** topic using `counter_party.py`.

---

### Stage 3 — NSE Exchange processes events  
`nse_exchange_consumer.py` listens to:

- `Trade_Order`  
- `Counter_party`

Once both are received, it triggers **nse_exchange_producer.py**, which generates:

- **DEMAT allocation** → published to `Demat_allocation`  
- **Cash movement** → published to `Cash_movement`

---

### Stage 4 — HDFC Broker receives settlement  
`hdfc_broker_consumer.py` consumes the final outputs:

- `DEMAT 100 SBI`  
- `DEBIT 98500`

---

## Architecture Overview

This project uses **four Kafka topics** to simulate a real-world stock settlement pipeline:

| Topic Name         | Producer Script            | Consumer Script            | Purpose                          |
|-------------------|----------------------------|----------------------------|----------------------------------|
| `Trade_Order`      | hdfc_broker_producer.py    | nse_exchange_consumer.py   | Captures trade requests          |
| `Counter_party`    | counter_party.py           | nse_exchange_consumer.py   | Confirms counter-party activity  |
| `Demat_allocation` | nse_exchange_producer.py   | hdfc_broker_consumer.py    | Sends demat allocation           |
| `Cash_movement`    | nse_exchange_producer.py   | hdfc_broker_consumer.py    | Sends cash debit movement        |

---

## Features Implemented

✔ Real-time multi-system communication  
✔ Event-driven processing  
✔ End-to-end message flow  
✔ Microservice-style separation (individual .py scripts)  
✔ Built on Kafka 4.x (KRaft mode, no ZooKeeper)  
✔ JSON-formatted messages for interoperability  

---

## Running the System

### 1. Start Kafka (KRaft Mode)
Format storage, start server, then create 4 topics:

- Trade_Order
- Counter_party
- Demat_allocation
- Cash_movement


---

### 2. Start the services (6 terminals recommended)

| Terminal | Script                     | Function                        |
|---------|----------------------------|----------------------------------|
| 1       | Kafka server               | Starts broker & controller       |
| 2       | Topic creation             | Run `kafka-topics.sh`            |
| 3       | nse_exchange_consumer.py   | Core processor                   |
| 4       | hdfc_broker_consumer.py    | Receives final outputs           |
| 5       | hdfc_broker_producer.py    | User sends trade order           |
| 6       | counter_party.py           | Sends confirmation               |

---

### 3. Example Input Flow

**Terminal 5 (Broker Producer):**
- 100,SBI,985

**Terminal 6 (Counter-party):**
- CONFIRM


---

### 4. Expected Outputs (HDFC Broker Consumer)
- DEMAT 100 SBI
- DEBIT 98500


---

## Conclusion

This project demonstrates how **Apache Kafka** can be used to build a **real-time financial transaction processing pipeline**, closely resembling real-world brokerage and stock exchange communication.

Key takeaways:

- Kafka ensures **low-latency**, **high-throughput**, **fault-tolerant** processing.  
- Event-driven microservices decouple all actors (Broker, Exchange, Counter-party).  
- Business logic (DEMAT + Cash movement) is triggered automatically through event streams.  
- The architecture is scalable and production-ready.

Overall, this project is a practical example of applying **real-time streaming systems** to financial trade workflows.

---

## Author

- **Arindam Paul**  
  [LinkedIn](https://www.linkedin.com/in/arindam-paul-19a085187/)

