from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Entry(Page):
    form_model = models.Player
    form_fields = ["guess"]



class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoff()


class Results(Page):

    def vars_for_template(self):
        current_id = self.player.id_in_group
        player = self.group.get_player_by_id(current_id)
        return {
            'result': '%.2f'.format(self.group.result),
            'guess': player.guess,
            'other_players': [p for p in self.group.get_players() if p.id_in_group != current_id],
            'payoff': player.payoff,
        }


page_sequence = [
    Entry,
    ResultsWaitPage,
    Results
]
