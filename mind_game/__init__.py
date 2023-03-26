from otree.api import *

doc = """
This app is a replication of mind game (Ting Jiang, 2013), and the version is throw-first version.

Procedures:
1. participants choose a side ("up" or "down") in mind
2. roll a dice once virtually, get the outcome
3. report the chosen side ("up" or "down")
4. Payment: only pay for reported side at step 3
   if the dice outcome is x, then report "up" can get x and  report "up" can get (7-x)

Pages:
- instruction: how the game will play
- comprehension: comprehension test questions
- choose_side: let people choose a side in mind 
- roll_dice: roll the dice and get the dice number
- report_side: show the dice number and let participants report the side as "side"
- Results: show the payoff
- complete: the introduce the next round, or present congrats at the final round.

"""


class C(BaseConstants):
    NAME_IN_URL = 'mind_game'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Questions in Comprehension Test
    q0_1 = models.IntegerField(label="The 'Up' side refer to the number: ")
    q0_2 = models.IntegerField(label="The 'Down' side refer to the number: ")
    q1 = models.IntegerField(label="If the participant A choose to report 'Up', the payoff in this round is:")
    q2 = models.IntegerField(label="If the participant A choose to report 'Down', the payoff in this round is:")

    dice_number = models.IntegerField(min=1, max=6)
    chosen = models.BooleanField(label="Have you already chosen a side?",
                                 choices=[[True, 'Yes'], [False, 'No']],
                                 widget=widgets.RadioSelectHorizontal)

    mind_side = models.IntegerField(label="Please report the chosen side in your mind",
                                    choices=[[1, 'Up'], [0, 'Down']],
                                    widget=widgets.RadioSelectHorizontal)


# PAGES
class instruction0(Page):
    # only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class instruction(Page):
    # only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class comprehension(Page):
    # only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['q0_1', 'q0_2', 'q1', 'q2', ]

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(q0_1=2, q0_2=5, q1=2, q2=5, )
        # error_message can return a dict whose keys are field names and whose values are error messages
        errors = {f: 'Please reconsider the answer here' for f in solutions if values[f] != solutions[f]}
        # print('errors is', errors)
        if errors:
            return errors


class understand(Page):
    # only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class roll_dice(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(dice_number=player.dice_number)


class result_pay(Page):
    pass


class choose_side(Page):
    form_model = 'player'
    form_fields = ['chosen']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # pre-determine the dice outcome randomly
        import random
        random_integer = random.randint(1, 6)
        player.dice_number = random_integer

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(chosen=True)
        # error_message can return a dict whose keys are field names and whose values are error messages
        errors = {f: 'Please choose a side in your mind' for f in solutions if values[f] != solutions[f]}
        # print('errors is', errors)
        if errors:
            return errors


class report_side(Page):
    form_model = 'player'
    form_fields = ['mind_side']

    @staticmethod
    def vars_for_template(player: Player):
        dice_number = player.dice_number
        return dict(dice_number=dice_number)


class Wait(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # determine and store the payoff before
        if player.mind_side == 1:
            player.payoff += player.dice_number
        if player.mind_side == 0:
            player.payoff += (7 - player.dice_number)


class next(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number != C.NUM_ROUNDS


class complete(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        total_pay = player.participant.payoff
        return dict(total_pay=total_pay)


page_sequence = [instruction0, instruction, comprehension, understand, choose_side, roll_dice, report_side, Wait, result_pay, next, complete]
