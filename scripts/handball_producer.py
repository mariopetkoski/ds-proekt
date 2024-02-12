import json, random, time
from confluent_kafka import Producer

from handball.data_generator import generate_teams

kafka_topic = "handball_matches"
conf = {"bootstrap.servers": "localhost:9092"}  # Adjust your Kafka configuration as needed
producer = Producer(conf)
teams = generate_teams(10)  # Generating 10 handball teams

def_probabilities = {
    "Foul": 0.2,
    "2-minute Suspension": 0.05,
    "Save": 0.15,
    "Goal": 0.4,  # Higher chance of scoring in handball
}

def get_event():
    event, prob = random.choice(list(def_probabilities.items()))
    return event if random.random() < prob else "No Event"

def create_json(player, team, event):
    return {
        "Player": player.name,
        "Number": player.number,
        "Team": team.name,
        "Event": event,
    }

def send_message(the_json):
    json_msg = json.dumps(the_json)
    producer.produce(kafka_topic, value=json_msg.encode("utf-8"))
    producer.flush()
    producer.poll(0)

for match in range(5):  # Simulate 5 matches
    team1, team2 = random.sample(teams, 2)
    print(f"Match: {team1.name} vs. {team2.name}")
    for minute in range(1, 61):  # Handball matches are typically 60 minutes
        for team in [team1, team2]:
            event = get_event()
            if event != "No Event":
                player = random.choice(team.players)
                msg = create_json(player, team, event)
                send_message(msg)
                print(f"Minute {minute}: {event} by {player.name} of {team.name}")
        time.sleep(1)  # Simulate real-time by waiting between events

producer.flush()
