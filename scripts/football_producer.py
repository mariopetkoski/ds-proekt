import json, random, time
from confluent_kafka import Producer

from football.data_generator import generate_teams


kafka_topic = "football_games"
conf = {"bootstrap.servers": "localhost:9092,localhost:9094,localhost:9096"}
producer = Producer(conf)
teams = generate_teams(8) # quarter finals

MINUTES = 90
SWAP_ATTACK_EVENTS = ["Steal", "Own Goal", "Offside", "Miss", "Goal"]

# add all soccer events here with probabilities of happening
# sum should go up to 1, preferrably with some space left for "no event"
# if the sum of probs of events reaches 1, all events after them are impossible to reach
def_probabilities = {
    "Yellow Card" : 0.1,
    "Red Card" : 0.05,
    "Foul" : 0.2,
    "Steal" : 0.35, # switch
    "Own Goal" : 0.001, # switch
}

atk_probabilities = {
    "Pass" : 0.6,
    "Miss" : 0.15, # switch
    "Goal" : 0.1, # switch
}

def pick_new_random(current, all):
    while True:
        new = random.choice(all)
        if(new.name != current.name):
            break
    return new

def get_event(probabilities: dict[str, float]):
    rand_num = random.random()
    cumulative_prob = 0
    for event, prob in probabilities.items():
        cumulative_prob += prob
        if rand_num < cumulative_prob:
            return event
    return None

def generate_event(team):
    probabilities = {}
    probabilities = atk_probabilities if team.is_attacking else def_probabilities
    return get_event(probabilities)

def switch_attacking(team1, team2):
    team1.is_attacking = not team1.is_attacking
    team2.is_attacking = not team2.is_attacking

# TODO change logic for OpenSearch graphs
def create_json(player, team, event):
    return {
        "Player": player.name,
        "Number": player.number,
        "Team": team.name,
        "Event": event,
    } if event not in ["Goal", "Miss"] else {
        "Player": player.name,
        "Number": player.number,
        "Team": team.name,
        "Event": event,
    }

def event_handler(this_player, other_player, event, this_team, other_team):
    if event is None: return this_player, other_player
    print(f"Player: {this_player.name}\tTeam: {this_team.name}\tEvent: {event}\tOther: {other_player.name}\tEnemy team: {other_team.name}")
    msg = create_json(this_player, this_team, event)
    send_message(msg)
    if event in SWAP_ATTACK_EVENTS:
        switch_attacking(this_team, other_team)
    this_player, other_player = pick_new_random(this_player, this_team.players), pick_new_random(other_player, other_team.players)
    
    return this_player, other_player

def send_message(the_json):
    if the_json is None: return
    json_msg = json.dumps(the_json)
    producer.produce(kafka_topic, value=json_msg.encode("utf-8"))
    producer.flush()
    producer.poll(1)

def print_players(team):
    print(f"Team \"{team.name}\" roster:\n")
    for player in team.players:
        print(f"Name: {player.name}, Number: {player.number}\n")
    print("\n\n\n\n\n")

while True:
    events_count = MINUTES
    team1 = random.choice(teams)
    team1.is_attacking = True
    team2 = pick_new_random(team1, teams)
    print(f"===  {team1.name} vs. {team2.name}  ===\n")
    print_players(team1)
    print_players(team2)
    try:
        team1_active_player = team1.players[0]
        team2_active_player = team2.players[0]
        # Produce messages
        for i in range(events_count):
            event1 = generate_event(team1)
            team1_active_player, team2_active_player = event_handler(team1_active_player, team2_active_player, event1, team1, team2)
            event2 = generate_event(team2)
            team2_active_player, team1_active_player = event_handler(team2_active_player, team1_active_player, event2, team2, team1)
            time.sleep(5) # Wait 5 seconds then create new event

        print(f"Produced {i*2} messages to Kafka topic: {kafka_topic} for {team1} vs. {team2}")

    except Exception as e:
        print(f"Exception while producing messages: {e}")

    finally:
        # Close the producer to release resources
        producer.flush()  # Ensure any remaining messages are delivered
    time.sleep(30) # Wait 30 seconds then launch a new game
