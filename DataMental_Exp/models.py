from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from random import randint

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Lying_Game'
    players_per_group = None
    num_rounds = 40


class Subsession(BaseSubsession):
    def creating_session(self):
        for jugador in self.get_players():
            jugador.numero_real = randint(1,6)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    numero_ingresado = models.IntegerField(min=1, max=6)
    numero_real = models.IntegerField(min=1, max=6)

    def set_payoff(self):
        self.payoff = self.numero_ingresado