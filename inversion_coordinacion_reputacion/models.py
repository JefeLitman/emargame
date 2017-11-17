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
    num_rounds = 2

    pago=c(1000)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def calcular_gananancia(self,p1inversion,p2inversion):
            ganancia=p1inversion*p2inversion/500
            return ganancia


class Player(BasePlayer):
    inversion=models.CurrencyField(initial=c(0),choices=currency_range(0,Constants.pago,c(1)))
    calificacion=models.IntegerField(initial=0, min=0, max=5)
    calificacion_promedio=models.FloatField(initial=0,min=0,max=5)
    ganancia_total = models.CurrencyField(initial=c(0))

    def set_payoff(self,ganancia):
        self.payoff=Constants.pago-self.inversion+ganancia

    def get_calificacion(self,nota):
        return self.calificacion
    def get_ganancias(self):
        return self.ganancia_total