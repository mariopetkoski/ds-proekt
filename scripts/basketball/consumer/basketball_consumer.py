from confluent_kafka import Consumer, KafkaException
from opensearchpy import OpenSearch
import json
import sys
import requests

# Kafka configuration
conf_kafka = {
    "bootstrap.servers": "broker1:9091,broker2:9093,broker3:9095",  # Update with your Kafka broker information
    "group.id": "basketball-analytics",
    "session.timeout.ms": 6000,
    "auto.offset.reset": "earliest",
    "enable.auto.offset.store": False,
}

c = Consumer(conf_kafka)

# OpenSearch configuration
es = OpenSearch(
    [{"host": "opensearch", "port": 9200, "scheme": "http"}],
    headers={"Content-Type": "application/json"},
)

# Index configuration for basketball analytics
index_name = "basketball_analytics"
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

topics = ["basketball_games"]
c.subscribe(topics, on_assign=print_assignment)

# TODO uncomment for ndjson config
# opensearch_url = "http://opensearch-dashboards:5601/api/saved_objects/_import?createNewCopies=true"
# ndjson_file = "basketball_index_and_dashboards.ndjson"  # Ensure this file has basketball-specific visualizations

# with open(ndjson_file, "rb") as f:
#     files = {"file": f}
#     headers = {"osd-xsrf": "true"}
#     response = requests.post(opensearch_url, files=files, headers=headers)

# if response.status_code == 200:
#     print("Opensearch Dashboard successfully configured for Basketball")
# else:
#     print(f"Error: {response.status_code} - {response.text}")

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
