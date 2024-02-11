import random, itertools

from models import Player, Team

# maximum of 15x3x15 = 675 possible player names
def generate_random_names():
    common_names = ["Jovan", "Emil", "Mihail", "Oliver", "Trajko", "Alek", "Vlado", "Stefan", "Branko", "Boris", "Robert", "Andrej", "Daniel", "Dario", "Spiro"]
    middle_names = [" ", " Hadzi ", " Pop "]
    common_surnames = ["Spirovski", "Jovanov", "Atanasovski", "Kolev", "Stojanov", "Trenevski", "Miloshevski", "Petkovski", "Dimitrov", "Andonovski", "Petrov", "Trajkovski", "Martinovski", "Dobrevski", "Iliev"]

    res = [''.join(comb) for comb in itertools.product(common_names, middle_names, common_surnames)]
    random.shuffle(res)
    return res

all_names = generate_random_names()

def pick_names(num_names):
    random_names = [all_names.pop() for _ in range(num_names)]
    random.shuffle(all_names)
    return random_names

# maximum of 5x10 = 50 teams
def generate_random_team_names():
    first_names = ["Skopje", "Ohrid", "Shtip", "Kumanovo", "Veles"]
    second_names = ["Spartans", "Knights", "Warriors", "Vikings", "Ninjas", "Wolves", "Tigers", "Eagles", "Raptors", "Bears"]

    res = [' '.join(comb) for comb in itertools.product(first_names, second_names)]
    random.shuffle(res)
    return res

all_teams = generate_random_team_names()

def pick_teams(num_teams):
    random_teams = [all_teams.pop() for _ in range(num_teams)]
    return random_teams

def generate_teams(num_teams):
    assert num_teams > 0 and num_teams <= 50

    # assume 11 players per team
    team_names = pick_teams(num_teams)
    random_teams = []

    for i in range(num_teams):
        player_names = pick_names(11)
        players = []
        numbers = random.sample(list(range(100)), 11)

        for name in player_names:
            players.append(Player(name, numbers.pop()))

        random_teams.append(Team(team_names[i], players))

    return random_teams