from otree.api import *



doc = """
This app is a replication of mind game throw-first version (Ting Jiang, 2013) + uncertain payoff adjustment

Procedures:
1. participants choose a side ("up" or "down") in mind
2. roll a dice once virtually, get the outcome
3. report the chosen side ("up" or "down")
4. the computer either increase or decrease "scale" points to the payoff
4. Payment: reported side + payoff adjustment
   if the dice outcome is x, then report "up" can get x and  report "up" can get (7-x)

Pages:
- instruction: how the game will play
- comprehension: comprehension test questions
- choose_side: let people choose a side in mind 
- roll_dice: roll the dice and get the dice number
- report_side: show the dice number and let participants report the side as "side"
- adjust_pay: calculate adjustments here
- result_pay: show the result of the final payment
- complete: the introduce the next round, or present congrats at the final round.

"""


class C(BaseConstants):
    NAME_IN_URL = 'mindgame_uncertain'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    scale = 3

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Questions in Comprehension Test
    q3 = models.IntegerField(min = -4, max = 11, label="If the dice outcome is 5, and participant A choose to report side 'Down', and the payoff adjustment turn out to be +5 points. What is the earning of participant A in this round?")
    q4 = models.IntegerField(min = -4, max = 11, label="If the dice outcome is 1, and participant A choose to report side 'Up', and the payoff adjustment turn out to be -5 points. What is the earning of participant A in this round?")
    
    dice_number = models.IntegerField(min=1, max=6)
    chosen = models.BooleanField(label="Have you already chosen a side?",
                                choices=[[True, 'Yes'], [False, 'No']],
                                widget=widgets.RadioSelectHorizontal
                                    )
    mind_side = models.IntegerField(label="Please report the chosen side in your mind: ",
                                choices=[[1, 'Up'], [0, 'Down']],
                                widget=widgets.RadioSelectHorizontal
                                    )
    change = models.IntegerField()
    random_number1 = models.FloatField(min=0, max=1)
    random_number2 = models.FloatField(min=0, max=1)
    payoff_before = models.IntegerField()
    payoff_after = models.IntegerField()

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
    form_fields = ['q3', 'q4', ]
    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(q3 = 7, q4= -4)
        # error_message can return a dict whose keys are field names and whose values are error messages
        errors = {f: 'Please reconsider your answer.' for f in solutions if values[f] != solutions[f]}
        # print('errors is', errors)
        if errors:
            return errors

class understand(Page):
    # only show in the first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class choose_side(Page):
    form_model = 'player'
    form_fields = ['chosen']
    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict( chosen = True)
        # error_message can return a dict whose keys are field names and whose values are error messages
        errors = {f: 'Please choose a side in your mind' for f in solutions if values[f] != solutions[f]}
        # print('errors is', errors)
        if errors:
            return errors
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # pre-determine the dice outcome randomly
        import random
        random_integer = random.randint(1, 6)
        player.dice_number = random_integer

class roll_dice(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(dice_number = player.dice_number)

class report_side(Page):
    form_model = 'player'
    form_fields = ['mind_side']
    @staticmethod
    def vars_for_template(player: Player):
        dice_number = player.dice_number
        return dict(dice_number = dice_number)

class adjust_pay(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # determine and store the payoff before
        if player.mind_side == 1:
            player.payoff += player.dice_number
            player.payoff_before = player.dice_number
        if player.mind_side == 0:
            player.payoff += (7-player.dice_number)
            player.payoff_before = (7-player.dice_number)
        
        # determine the payoff adjustment
        # Adjustment: ambiguity
        import random
        player.random_number1 = random.random()
        player.random_number2 = random.random()
        if player.random_number1 >= player.random_number2:
            player.change = C.scale
        else:
            player.change = C.scale*(-1)
        player.payoff += player.change
        player.payoff_after = player.payoff_before + player.change

class result_pay(Page):
    pass

class next(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number != C.NUM_ROUNDS

        
page_sequence = [instruction0, instruction, comprehension, understand, choose_side, roll_dice, report_side, adjust_pay, result_pay, next]
