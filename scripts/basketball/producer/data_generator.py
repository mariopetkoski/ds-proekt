import random
import itertools

from models import Player, Team
# Player and Team class definitions remain the same as provided earlier

# Generates a large pool of random player names
def generate_random_names():
    common_names = ["Jordan", "LeBron", "Kobe", "Kevin", "Stephen", "James", "Anthony", "Russell", "Kyrie", "Damian"]
    middle_names = ["", " Jr.", " Sr."]
    common_surnames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]

    res = [''.join(comb) for comb in itertools.product(common_names, middle_names, common_surnames)]
    random.shuffle(res)
    return res

all_names = generate_random_names()

def pick_names(num_names):
    random_names = [all_names.pop() for _ in range(num_names)]
    random.shuffle(all_names)  # Optional: Shuffle remaining names to ensure variety
    return random_names

# Generates a list of unique team names
def generate_random_team_names():
    city_names = ["New York", "Los Angeles", "Chicago", "Houston", "Miami", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas"]
    team_nicknames = ["Eagles", "Sharks", "Wizards", "Giants", "Lions", "Bulls", "Hawks", "Stars", "Knights", "Rangers"]

    res = [' '.join(comb) for comb in itertools.product(city_names, team_nicknames)]
    random.shuffle(res)
    return res

all_teams = generate_random_team_names()

def pick_teams(num_teams):
    random_teams = [all_teams.pop() for _ in range(num_teams)]
    random.shuffle(all_teams)  # Optional: Shuffle remaining names to ensure variety
    return random_teams

# Generates a specified number of teams with players
def generate_teams(num_teams):
    assert num_teams > 0 and num_teams <= len(all_teams), "Number of teams must be within the range of available team names."

    team_names = pick_teams(num_teams)
    random_teams = []

    for team_name in team_names:
        player_names = pick_names(5)  # Assuming 5 players for a starting lineup in basketball
        players = [Player(name, random.randint(0, 99)) for name in player_names]  # Assign random jersey numbers

        random_teams.append(Team(team_name, players))

    return random_teams
