from otree.api import Bot
from . import *

class PlayerBot(Bot):
    def play_round(self):
        yield instruction
        yield comprehension, dict(q0_1=2, q0_2=5, q1=2, q2=5)
        yield choose_side, dict(choose_side = 1)
        yield roll_dice

instruction, comprehension, choose_side, roll_dice, report_side, Wait, result_pay, next, complete