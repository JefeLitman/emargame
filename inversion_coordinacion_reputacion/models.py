from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'inversion_coordinacion_reputacion'
    players_per_group = 2
    num_rounds = 1

    pago=c(1000)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def calcular_gananancia(self,p1inversion,p2inversion):
            ganancia=p1inversion*p2inversion/500
            return ganancia


class Player(BasePlayer):
    inversion=models.CurrencyField(initial=c(0),min=c(0),max=c(0))
    calificacion=models.IntegerField(initial=0, min=0, max=5)

    def set_payoff(self,ganancia):
        self.payoff=Constants.pago-self.inversion+ganancia

    def obtener_inversion(self):
        return self.inversion