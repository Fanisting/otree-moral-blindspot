from otree.api import Bot
from . import *

class PlayerBot(Bot):
    def play_round(self):
        
        yield Welcome, dict(prolific_id='test_bot')
        yield Consent_Form

        