import random, itertools

# Assuming models.py has the same Player and Team classes
from models import Player, Team

def generate_random_names():
    # Names and surnames adapted for diversity and typical handball nations
    first_names = ["Liam", "Emma", "Noah", "Olivia", "Ethan", "Ava", "Mason", "Sophia", "Logan", "Isabella"]
    middle_initials = ["", " J.", " M.", " B.", " T."]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]

    res = [''.join(comb) for comb in itertools.product(first_names, middle_initials, last_names)]
    random.shuffle(res)
    return res

all_names = generate_random_names()

def pick_names(num_names):
    return [all_names.pop() for _ in range(num_names)]

def generate_random_team_names():
    city_names = ["Capital", "Riverside", "Mountain", "Lakeside", "Seaside"]
    mascots = ["Eagles", "Wolves", "Tigers", "Sharks", "Dragons"]

    res = [' '.join(comb) for comb in itertools.product(city_names, mascots)]
    random.shuffle(res)
    return res

all_teams = generate_random_team_names()

def pick_teams(num_teams):
    return [all_teams.pop() for _ in range(num_teams)]

def generate_teams(num_teams):
    assert 0 < num_teams <= 50  # Adjusted for potential upper limit of unique team names

    team_names = pick_teams(num_teams)
    random_teams = []

    for name in team_names:
        player_names = pick_names(7)  # Adjusted for 7 players in a handball team
        players = [Player(name, random.randint(1, 99)) for name in player_names]

        random_teams.append(Team(name, players))

    return random_teams
