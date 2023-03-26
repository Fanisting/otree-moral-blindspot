from otree.api import Bot
from . import *

class PlayerBot(Bot):
    def play_round(self):
        yield survey, dict(gender=1, age=1, edu=1, religion=1)
        yield Finished
