import random

class Dice:
    def __init__(self, idnum: int):
        self.idnum = idnum
        self.state = None
    
    def roll(self):
        R = random.randint(1,6)
        self.state = R
        return self