from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random


author = 'Allen Ma'

doc = """
My version of Guess 2/3rd of the average
"""


class Constants(BaseConstants):
    name_in_url = 'my_guess_average'
    players_per_group = 3
    num_rounds = 1


class Subsession(BaseSubsession):

    def creating_session(self):
        pass


class Group(BaseGroup):
    def calc_avg(self):
        total = 0
        for player in self.get_players():
            total += player.guess
        twothird_average = 2/3 * (total / Constants.players_per_group)
        return twothird_average

    def check_same(self):
        for i in range(len(self.get_players())):
            if i == Constants.players_per_group - 1:
                break
            player = self.get_players()[i]
            player_next = self.get_players()[i+1]
            if not (player_next.guess == player.guess):
                return None
        return [1 for _ in range(Constants.players_per_group)]

    def check_two(self):
        # hardcode player 1, 2 and 3
        player1 = self.get_player_by_id(1)
        player2 = self.get_player_by_id(2)
        player3 = self.get_player_by_id(3)

        result = self.calc_closest()

        # check if any two guesses are the same
        if (player1.guess == player2.guess and player1.guess != player3.guess):
            if abs(player3.guess - result) < abs(player1.guess - result):
                return [1,1,0]
            else:
                return [0, 0, 1]
        elif (player2.guess == player3.guess and player1.guess != player3.guess):
            if abs(player3.guess - result) < abs(player1.guess - result):
                return [0, 1, 1]
            else:
                return [1, 0, 0]
        elif (player3.guess == player1.guess) and player1.guess != player2.guess:
            if abs(player1.guess - result) < abs(player2.guess - result):
                return [1, 0, 1]
            else:
                return [0, 1, 0]

        return None

    def check_winner(self):

        # assumes that there is only one winner
        # and that each guess is unique
        dist = 100
        index = 1
        result = self.calc_closest()
        for player in self.get_players():
            if abs(player.guess - result) < dist:
                dist = abs(player.guess - result)
                index = player.id_in_group
        return index

    def calc_closest(self):
        """"returns ID of player with the closest guess"""


        # if three players have the same guess, then return a list with [1,1,1]
        # if two players have the same guess, then return [1,1,0] if they won,
        # and [0, 0, 1] if they lost, for example
        # otherwise, just return a list with 1 for the index of the best player

        same_index = self.check_same()
        if same_index:
            return same_index

        two_index = self.check_two()
        if two_index:
            return two_index

        winner_index = self.check_winner()
        if winner_index:
            return winner_index

        raise Exception("no outcome found")

    def set_payoff(self):
        winner_list = self.calc_closest()
        for i in range(Constants.players_per_group):
            if winner_list[i] == 1:
                player = self.get_player_by_id(i+1)
                player.payoff = c(100)
            else:
                player.payoff = c(0)


class Player(BasePlayer):
    payoff = c(0)
    guess = models.IntegerField(initial=0,min=0, max=100)



