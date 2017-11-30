from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'señales'
    players_per_group = None
    num_rounds = 20


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    def role(self):
        if self.id_in_group == 1:
            return 'Vendedor'
        if self.id_in_group == 2:
            return 'Comprador'