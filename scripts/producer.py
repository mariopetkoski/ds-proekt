from confluent_kafka import Producer
import json
import random
from data_generator import athlete_names, sports_list,countries_names

kafka_topic = "topic-1"
# Kafka producer configuration
conf = {"bootstrap.servers": "localhost:9092,localhost:9094,localhost:9096"}

# Create a single instance of the producer
producer = Producer(conf)

try:
    # Produce messages
    for i in range(3):
        # Produce a message to the Kafka topic
        random_athlete = {
            "athleteId": random.randint(1000, 9999),
            "name": random.choice(athlete_names),
            "sport": random.choice(sports_list),
            "height": round(random.uniform(1.60, 2.40), 2),
            "nationality": random.choice(countries_names),
            "age": random.randint(16, 45)
        }
        json_message = json.dumps(random_athlete)

        producer.produce(kafka_topic, value=json_message.encode("utf-8"))

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
