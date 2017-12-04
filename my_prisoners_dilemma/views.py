from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.run_choice_logic()


class Results(Page):

    def vars_for_template(self):
        current_id = self.player.id_in_group
        players = self.group.get_players()
        for player in players:
            if current_id != player.id_in_group:
                other_player = player

        return {
            'choice': self.player.get_prisoner_choice_display(),
            # the other player's choice
            'other_choice': other_player.get_prisoner_choice_display(),
            'player_result': self.player.player_result,
        }

class Choice(Page):
    form_model = models.Player
    form_fields = ['prisoner_choice']




page_sequence = [
    Choice,
    ResultsWaitPage,
    Results
]
