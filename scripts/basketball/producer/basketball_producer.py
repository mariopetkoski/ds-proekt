import json
import random
import time
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

from data_generator import generate_teams

# Assuming the `Team` and `Player` classes are defined as before

# Utility functions for generating names remain unchanged
# generate_random_names, pick_names, generate_random_team_names, pick_teams

teams = generate_teams(8)  # for quarter finals in a basketball tournament

# Basketball game specifics
QUARTERS = 4
TIME_PER_QUARTER = 12  # in minutes, for simulation purposes
BASKETBALL_EVENTS = ["Two-Point Score", "Three-Point Score", "Free Throw", "Rebound", "Steal", "Foul", "Turnover"]
EVENT_PROBABILITIES = {
    "Two-Point Score": 0.3,
    "Three-Point Score": 0.15,
    "Free Throw": 0.1,
    "Rebound": 0.2,
    "Steal": 0.05,
    "Foul": 0.1,
    "Turnover": 0.1,
}

kafka_topic = "basketball_games"
conf = {"bootstrap.servers": "broker1:9091, broker2:9093, broker3:9095"}
num_partitions = 3
num_replication = 3
admin_client = AdminClient(conf)
new_topic = NewTopic(kafka_topic, num_partitions, num_replication)
admin_client.create_topics([new_topic])
producer = Producer(conf)

def get_basketball_event():
    rand_num = random.random()
    cumulative_prob = 0
    for event, prob in EVENT_PROBABILITIES.items():
        cumulative_prob += prob
        if rand_num < cumulative_prob:
            return event
    return "No Event"

def create_basketball_json(player, team, event):
    return {
        "Player": player.name,
        "Number": player.number,
        "Team": team.name,
        "Event": event,
    }

def send_message(the_json):
    if the_json is None: return
    json_msg = json.dumps(the_json)
    producer.produce(kafka_topic, value=json_msg.encode("utf-8"))
    producer.flush()
    producer.poll(1)

while True:
    team1, team2 = random.sample(teams, 2)
    for quarter in range(QUARTERS):
        print(f"Quarter {quarter + 1}: {team1.name} vs. {team2.name}")
        for minute in range(TIME_PER_QUARTER):
            for team in [team1, team2]:
                player = random.choice(team.players)
                event = get_basketball_event()
                msg = create_basketball_json(player, team, event)
                send_message(msg)
                print(f"Minute {minute + 1} - {team.name} - {player.name}: {event}")
            time.sleep(1)  # Simulating time passage more quickly
    time.sleep(10)  # Wait before starting a new set of quarters
