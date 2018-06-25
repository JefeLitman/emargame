from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint,random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'buscadores_renta'
    players_per_group = None
    num_rounds = 30
    dotacion=c(500)

class Subsession(BaseSubsession):

    def seleccionar_ganador_subasta(self):
        jugadores=self.get_players()
        inversion_jugadores=[]
        for i in range(len(jugadores)):
            inversion_jugadores.append(jugadores[i].da_invertir+random())
        for i in range(len(inversion_jugadores)):
            if inversion_jugadores[i] == max(inversion_jugadores):
                jugadores[i].gano=True

    def seleccionar_ganador_loteria(self):
        jugadores=self.get_players()
        inversionistas=[]
        for i in range(len(jugadores)):
            if jugadores[i].da_invertir != c(0):
                inversionistas.append(jugadores[i])
        inversionistas[randint(0,len(inversionistas))].gano=True

    def calcular_valores_productos(self):
        jugadores=self.get_players()
        for i in jugadores:
            i.calcular_valor_producto()

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    da_invertir=models.CurrencyField(initial=c(0),min=c(0),max=c(500))
    valor_producto=models.IntegerField(initial=0)
    ganancias_totales=models.CurrencyField(initial=c(0))
    gano=models.BooleanField(initial=False)

    def calcular_valor_producto(self):
        self.valor_producto=randint(1000,5000)

    def calcular_ganancias_totales(self):
        self.ganancias_totales=sum([p.c_privada for p in self.in_all_rounds()])

    def calcular_ganancia_ronda(self):
        if self.gano:
            self.payoff=Constants.dotacion-self.da_invertir+self.valor_producto
        else:
            self.payoff = Constants.dotacion - self.da_invertir