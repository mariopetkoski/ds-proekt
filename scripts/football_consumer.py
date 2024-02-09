from confluent_kafka import Consumer, KafkaException
from opensearchpy import OpenSearch
import json
import sys

# Kafka configuration
conf_kafka = {
    "bootstrap.servers": "localhost:9092,localhost:9094,localhost:9096",  # Update with your Kafka broker information
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
index_name = "football_analytics"
index_mapping = {
  "mappings": {
    "properties": {
      "Player": {
        "type": "keyword"
      },
      "Number": {
        "type": "keyword"
      },
      "Team": {
        "type": "keyword"
      },
      "Event": {
        "type": "keyword"
      },
    }
  }
}

# Ensure that the index exists with the specified mapping
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_mapping)

def print_assignment(consumer, partitions):
    print("Assignment:", partitions)

topics = ["football_games"]
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

            # Attempt to parse the JSON message
            try:
                message_dict = json.loads(message)  # Convert JSON string to Python dictionary
                # Index the message dictionary into OpenSearch
                es.index(index=index_name, body=message_dict)
                print("Message indexed into OpenSearch.")
            except json.JSONDecodeError as e:
                print(f"Error parsing message JSON: {e}")
            except Exception as e:
                print(f"Error indexing message into OpenSearch: {e}")

except KeyboardInterrupt:
    sys.stderr.write("%% Aborted by user\n")
finally:
    # Close Kafka consumer
    c.close()