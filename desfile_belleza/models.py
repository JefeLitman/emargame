from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Escoge el ganador que este a 2/3 de la media-
"""


class Constants(BaseConstants):
    name_in_url = 'desfile_belleza'
    players_per_group = None
    num_rounds = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    winner = models.CharField()

    def set_winner(self,jugadores):
        media = 0
        for i in range(0,len(jugadores),1):
            media=media+jugadores[i].elegido
        media=media/len(jugadores)
        ganador=(media*2)/3
        menor=100
        for i in range (0,len(jugadores),1):
            if (abs(jugadores[i].elegido - ganador) < menor):
                menor = abs(jugadores[i].elegido - ganador)
                indice_ganador = i
        self.winner=jugadores[indice_ganador].nombre_elegido


class Player(BasePlayer):
    elegido = models.PositiveIntegerField(initial=0)
    nombre_elegido = models.CharField()
