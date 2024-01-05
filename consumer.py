from confluent_kafka import Consumer, KafkaException
from opensearchpy import OpenSearch
import sys

# Kafka configuration
conf_kafka = {
    "bootstrap.servers": "localhost:9094",  # Update with your Kafka broker information
    "group.id": "consumer1",
    "session.timeout.ms": 6000,
    "auto.offset.reset": "earliest",
    "enable.auto.offset.store": False,
}

c = Consumer(conf_kafka)

# OpenSearch configuration
es = OpenSearch(
    [{"host": "localhost", "port": 9200, "scheme": "http"}],
    headers={"Content-Type": "application/json"},
)

# Index configuration
index_name = "test_index"
index_mapping = {"mappings": {"properties": {"message": {"type": "text"}}}}

# Ensure that the index exists with the specified mapping
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_mapping)

def print_assignment(consumer, partitions):
    print("Assignment:", partitions)

topics = ["topic-1"]
c.subscribe(topics, on_assign=print_assignment)

try:
    while True:
        msg = c.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            message = msg.value().decode("utf-8")
            print("Received message:", message)

            # Indexing message into OpenSearch
            try:
                es.index(index=index_name, body={"message": message})
                print("Message indexed into OpenSearch.")
            except Exception as e:
                print(f"Error indexing message into OpenSearch: {e}")

except KeyboardInterrupt:
    sys.stderr.write("%% Aborted by user\n")

finally:
    # Close Kafka consumer
    c.close()
