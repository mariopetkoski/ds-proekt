from confluent_kafka import Producer

message = "test"
kafka_topic = "topic-1"

# Kafka producer configuration
conf = {"bootstrap.servers": "localhost:9094"}

# Create a single instance of the producer
producer = Producer(conf)

try:
    # Produce messages
    for i in range(3):
        # Produce a message to the Kafka topic
        producer.produce(kafka_topic, value=message.encode("utf-8"))

        # Flush messages to ensure delivery
        producer.flush()

        # Wait for any outstanding messages to be delivered and delivery reports received
        producer.poll(1)

    print(f"Produced {i+1} messages to Kafka topic: {kafka_topic}")

except Exception as e:
    print(f"Exception while producing messages: {e}")

finally:
    # Close the producer to release resources
    producer.flush()  # Ensure any remaining messages are delivered
