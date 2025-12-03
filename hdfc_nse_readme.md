# Format the log directory using that ID (# new terminal_1)
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
echo "$KAFKA_CLUSTER_ID"

# The default config/server.properties already has:
# * process.roles=broker,controller
# * node.id=1
# * controller.quorum.voters=1@localhost:9093

bin/kafka-storage.sh format \
  -t "$KAFKA_CLUSTER_ID" \
  -c config/server.properties --standalone

# Starting the broker + controller. Leave this terminal open; it’s your broker+controller.
bin/kafka-server-start.sh config/server.properties

# If you ever need to stop it: Ctrl+C in that terminal, or use 
bin/kafka-server-stop.sh --process-role=broker.

# In Another Terminal - Creating a topic Trade_Order (# new terminal_2)
bin/kafka-topics.sh \
  --create \
  --topic Trade-Order \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# In Another Terminal - Creating a topic Counter_Party 
bin/kafka-topics.sh \
  --create \
  --topic Counter-Party  \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# In Another Terminal - Creating a topic Demat_Allocation 
bin/kafka-topics.sh \
  --create \
  --topic Demat-Allocation  \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# In Another Terminal - Creating a topic Cash_Movement 
bin/kafka-topics.sh \
  --create \
  --topic Cash-Movement  \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# List down the topics 
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Start nse_exchange_consumer (# new_terminal_3)
source kafka-env/bin/activate
python nse_exchange_consumer.py


# Start hdfc_broker_consumer (# new_terminal_4)
source kafka-env/bin/activate
python hdfc_broker_consumer.py


# Start hdfc_broker_producer (# new_terminal_5)
source kafka-env/bin/activate
python hdfc_broker_producer.py

# Type: 100,SBI,985 and press Enter.


# Start counter_party (# new_terminal_6)
source kafka-env/bin/activate
python counter_party.py

# Type: CONFIRM (or confirm) and press Enter.

# Send trade first, then confirmation:

# Terminal 5: send 100,SBI,985 → the NSE consumer stores pending_order.

# Terminal 6: send CONFIRM → NSE consumer processes pending_order and produces DEMAT & CASH. 
# Terminal 4 (HDFC consumer) prints the outputs.