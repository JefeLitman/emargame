from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'conflicto'
    players_per_group = 2
    num_rounds = 2


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    x=models.IntegerField(initial=randint(0, 500))
    y=models.IntegerField(initial=randint(500, 1500))
    opcion_azul = models.IntegerField(
        choices=[
            [0, 'A1'],
            [1, 'A2'],
        ],
        initial=1
    )
    opcion_verde = models.IntegerField(
        choices=[
            [0, 'V1'],
            [2, 'V2'],
        ],
        initial=2
    )

    def set_payoffs(self):
        jugador_azul = self.get_player_by_id(1)
        jugador_verde = self.get_player_by_id(2)
        matrix=[[1000,1000,self.x,self.y],[self.y,self.x,250,250]]
        jugador_azul.payoff=matrix[self.opcion_azul][self.opcion_verde]
        jugador_verde.payoff = matrix[self.opcion_azul][self.opcion_verde+1]

class Player(BasePlayer):
    ganancias_totales = models.CurrencyField(initial=c(0))

    def role(self):
        if self.id_in_group == 1:
            return 'Azul'
        if self.id_in_group == 2:
            return 'Verde'
