from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Allen Ma'

doc = """
One iteration of the classic prisoner's dilemma game
"""


class Constants(BaseConstants):
    name_in_url = 'my_prisoners_dilemma'
    players_per_group = 2
    num_rounds = 1
    # possible outcomes of the prisoner's dilemma game
    free_period = 0
    both_betray_period = 2
    betray_period = 3
    silent_period = 1


class Subsession(BaseSubsession):

    def creating_session(self):
        pass


class Group(BaseGroup):

    def run_choice_logic(self):
        player1 = self.get_player_by_id(1)
        player2 = self.get_player_by_id(2)

        if player1.prisoner_choice == 1 and player2.prisoner_choice == player1.prisoner_choice:
            # both betray
            player1.player_result = Constants.both_betray_period
            player2.player_result = Constants.both_betray_period
        elif player1.prisoner_choice == 2 and player2.prisoner_choice == player1.prisoner_choice:
            player1.player_result = Constants.silent_period
            player2.player_result = Constants.silent_period
        elif player1.prisoner_choice == 2 and player2.prisoner_choice == 1:
            player1.player_result = Constants.betray_period
            player2.player_result = Constants.free_period
        elif player1.prisoner_choice == 1 and player2.prisoner_choice == 2:
            player1.player_result = Constants.free_period
            player2.player_result = Constants.betray_period


class Player(BasePlayer):

    prisoner_choice = models.PositiveIntegerField(
        choices=[
            [1, 'betray'],
            [2, 'remain silent'],
        ],
        widget=widgets.RadioSelect
    )

    player_result = models.IntegerField()

