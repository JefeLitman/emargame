from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'signals'
    players_per_group = None
    num_rounds = 2
    valor = [c(500), c(1000), c(1500), c(2000), c(2500)]
    costo = [c(100), c(200), c(300), c(400), c(500)]


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    calidad_real=models.IntegerField(initial=0,min=1,max=5)
    calidad_ofrecida=models.IntegerField(initial=0,min=1,max=5)
    precio_vendedor=models.CurrencyField(initial=c(0))
    decision_comprador=models.BooleanField(initial=False,choices=[
        [True,'Si'],
        [False,'No']
    ])
    decision_vendedor = models.BooleanField(initial=False, choices=[
        [True, 'Si'],
        [False, 'No']
    ])

    def set_payoffs(self):
        vendedor=self.get_player_by_id(1)
        comprador=self.get_player_by_id(2)
        if(self.decision_comprador):
            comprador.payoff=Constants.valor[self.calidad_real-1]-self.precio_vendedor
            if(self.decision_vendedor):
                vendedor.payoff=self.precio_vendedor-Constants.costo[self.calidad_real-1]-c(500)
            else:
                vendedor.payoff = self.precio_vendedor - Constants.costo[self.calidad_real - 1]
        else:
            vendedor.payoff=c(0)
            comprador.payoff=c(0)



class Player(BasePlayer):

    def role(self):
        if self.id_in_group == 1:
            return 'Vendedor'
        if self.id_in_group == 2:
            return 'Comprador'