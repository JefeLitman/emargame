from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'keyne_beauty_context'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    winner=''

    def set_media(self):
        jugadores=self.get_players()
        n=len(jugadores)
        suma=0
        for i in range (0,n,1):
            suma=suma+jugadores[i].input_player
        media=suma/n
        valor_elegido=media*2/3

        menor=100
        for i in range (0,n,1):
            resta=abs(jugadores[i].input_player - valor_elegido)
            resta=resta+random.random()
            if (resta <= menor)
                menor = resta
                indice_ganador=i

        self.winner=jugadores[indice_ganador].name_player


class Player(BasePlayer):
    input_player = models.PositiveIntegerField(initial=0,min=0,max=100)
    name_player = models.CharField()
