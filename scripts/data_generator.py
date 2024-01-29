import requests
import random

countries_url = "https://countriesnow.space/api/v0.1/countries"
response = requests.get(countries_url)

if response.status_code == 200:
    countries_data = response.json()["data"]
    countries_names = [country["country"] for country in countries_data]
else:
    print(f"Failed to fetch countries data. Status code: {response.status_code}")
    exit()


def generate_random_names(num_names):
    common_names = ["John", "Emma", "Michael", "Olivia", "James", "Ava", "William", "Sophia", "Elijah", "Isabella"]
    common_surnames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]


    random_names = [f"{random.choice(common_names)} {random.choice(common_surnames)}" for _ in range(num_names)]

    return random_names

athlete_names = generate_random_names(100)

sports_list = [
    "Football",
    "Basketball",
    "Baseball",
    "Soccer",
    "Tennis",
    "Golf",
    "Hockey",
    "Volleyball",
    "Cricket",
    "Rugby",
    "Table Tennis",
    "Badminton",
    "Swimming",
    "Athletics",
    "Cycling",
    "Boxing",
    "Martial Arts",
    "Wrestling",
    "Skiing",
    "Snowboarding",
    "Surfing",
    "Rowing",
    "Canoeing",
    "Cycling",
    "Archery",
    "Gymnastics",
    "Weightlifting",
    "Fencing",
    "Equestrian",
    "Softball",
    "Handball",
    "Water Polo",
    "Darts",
    "Billiards",
    "Bowling",
    "Auto Racing",
    "Esports",
    "Yoga",
    "Pilates"
]
