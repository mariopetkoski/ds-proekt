class Team:
    def __init__(self, name, players):
        self.name, self.players, self.is_attacking = name, players, False
    
class Player:
    def __init__(self, name, number):
        self.name, self.number = name, number