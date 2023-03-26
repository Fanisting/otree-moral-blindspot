from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.IntegerField(label="What is your gender",
                                choices=[[1, 'Male'], [0, 'Female']],
                                widget=widgets.RadioSelectHorizontal
                            )
    age = models.IntegerField(label="What is your age", min = 0, max = 113)
    edu = models.IntegerField(label="What is your highest level education you have completed?", 
                                choices=[[1, 'Less than High School'], [2, 'High School / GED'], [3, 'Some College'], [4, '2-year College Degree'], [5, '4-year College Degree'], [6, 'Masters Degree'], [7, 'Doctoral Degree'], [8, 'Professional Degree (JD, MD)']],
                            )
    religion = models.IntegerField(label="What religious family do you belong to or identify yourself most close to?",
                                choices=[[1, 'Asian Folk Religion'], [2, 'Hindu'], [3, 'Jewish'], [4, 'Muslim'], [5, 'Christian (Catholic protestant or any other Christian denominations)'], [6, 'Other, I am not religious']],
                            )
    earned = models.FloatField()
    luck = models.BooleanField()
    link = models.StringField(default = "no_link_provided")

# PAGES
class survey(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'edu', 'religion']
    # determine the random payoff
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        p = 0.25 # the chance of bonus
        rand = random.random()
        if rand <= p:
            player.luck = True
            player.earned = float(player.participant.payoff_plus_participation_fee())
        else:
            player.luck = False
            player.earned = 4

class Finished(Page):
    pass

page_sequence = [survey, Finished]
