from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# Allen Ma
# November 2017
# For EC297 Experiment

author = 'Allen Ma'

doc = """
Rigidity of wages and effort through market cycles
"""

class Constants(BaseConstants):
    name_in_url = 'market_wage'
    players_per_group = 2
    num_rounds = 12

    # example: hardcoded
    # baseline -4
    # recession - 4
    # boom - 4
    # baseline - 4

    # 8 subperiods if you doubled the market sequence
    num_subperiods = 4

    # check that you can split num_rounds
    if not (num_rounds % num_subperiods == 0):
        raise ValueError("num_rounds and num_subperiods not evenly divisible")


    # hardcoded user periods
    SUBPERIODS = {
        "baseline": 3,
        "recession": 3,
        "boom": 3,
    }


    # hardcoded sequence
    # should be able to be modified by user
    MARKET_SEQUENCE = [
        "baseline",
        "recession",
        "boom",
        "baseline"
    ]

    # check that the market sequence subperiods add up to 12
    total_subperiods = 0
    for key in MARKET_SEQUENCE:
        total_subperiods += SUBPERIODS.get(key)
    if total_subperiods != num_rounds:
        raise ValueError("total subperiods {} does not equal number of rounds (12)".format(total_subperiods))

    # check that the periods sequence and the
    # market sequence matches in length
    if len(MARKET_SEQUENCE) != num_subperiods:
        raise ValueError("sequence in periods does not match num_subperiods")

    # a global dictionary that will take as a key:
    # the round number (1-indexed!)
    # and return the revenue for that particular round
    # eg. in the case of 12 rounds, and the sequence (baseline, boom, recession, baseline)
    # REVENUE[3] will return baseline; REVENUE[4] will return boom; REVENUE[8] will return recession

    # To construct the dictionary:
    # We use the market sequence mapping and an algorithm to determine the appropriate level

    # Note that we first set the value to a string, because in the creating session,
    # we access the config variables in self.session and set the appropriate  NUMERICAL VALUE
    REVENUE = {}
    for round in range(1, num_rounds + 1):
        running_total = 0
        for key in MARKET_SEQUENCE:
            running_total += SUBPERIODS.get(key)
            if running_total >= round:
                round_type = key
                break
        if round_type == "baseline":
            REVENUE[round] = "baseline"
        elif round_type == "boom":
            REVENUE[round] = "boom"
        elif round_type == "recession":
            REVENUE[round] = "recession"
        else:
            raise KeyError("level not found")

    # a global dictionary that will take as a key:
    # the round number (1-indexed!)
    # and return the category for that particular round
    REVENUE_CATEGORY = {}

    # copy the revenue dictionary before it gets modified in the creating session function
    REVENUE_CATEGORY = dict(REVENUE)


    COST_FUNCTION = {
        0.05: 1,
        0.10: 3,
        0.15: 5,
        0.20: 7,
        0.25: 10,
        0.30: 13,
        0.35: 17,
        0.40: 20,
        0.45: 24,
        0.50: 28,
        0.55: 33,
        0.60: 37,
        0.65: 42,
        0.70: 47,
        0.75: 52,
        0.80: 57,
        0.85: 63,
        0.90: 68,
        0.95: 74,
        1.00: 80,
    }

def cost_from_effort(effort):
    return Constants.COST_FUNCTION[effort]



class Subsession(BaseSubsession):

    def creating_session(self):

        self.session.vars['revenue'] = 1000
        init_revenue = self.session.config["base_revenue"]

        for key, value in Constants.REVENUE.items():
            if value == "baseline":
                Constants.REVENUE[key] = self.session.config["base_multiplier"] * init_revenue
            elif value == "recession":
                Constants.REVENUE[key] = self.session.config["recession_multiplier"] * init_revenue
                print("@@@@recession ", Constants.REVENUE[key])
            elif value == "boom":
                Constants.REVENUE[key] = self.session.config["boom_multiplier"] * init_revenue
            assert(type(Constants.REVENUE[key] == int))


class Group(BaseGroup):

    # max wage is dynamically set in views
    wage = models.PositiveIntegerField(
        doc="The wage the firm wants to set for the worker",
        widget=widgets.SliderInput(attrs={'step': '1'}),
    )

    effort = models.FloatField(
        min=0.05,
        max=1.00,
        doc="The effort level that the worker chooses",
        widget=widgets.SliderInput(attrs={'step': '0.05'})
    )

    def set_payoffs(self):
        firm = self.get_player_by_role('firm')
        worker = self.get_player_by_role('worker')

        # the formula for calculating the respective payoffs are as follows:
        # payoff(firm) = (revenue - wage) * effort
        # payoff(worker = revenue - cost(effort)
        firm.payoff = (Constants.REVENUE[self.round_number] - self.wage) * self.effort
        worker.payoff = self.wage - cost_from_effort(self.effort)

    def get_payoff_by_role(self, role):
        if role == 'firm':
            payoff = self.get_player_by_role("firm").payoff
            return payoff
        elif role == "worker":
            payoff = self.get_player_by_role("worker").payoff
            return payoff



class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return "firm"
        elif self.id_in_group == 2:
            return "worker"



