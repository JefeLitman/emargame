from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mercados_prohibidos'
    players_per_group = 2
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()

class Group(BaseGroup):
    from random import randint
    costo_producto=models.IntegerField(initial=randint(0,1000),blank=True)
    valoracion_cpu=models.IntegerField(initial=randint(1000,2000),blank=True)
    precio_vendedor=models.IntegerField(
        min=costo_producto,
        max=2000,
        initial=costo_producto
    )
    valoracion_comprador=models.IntegerField(
        min=0,
        max=valoracion_cpu,
        initial=0
    )
    revision=models.IntegerField(initial=randint(1,100),blank=True)

    def set_payoff(self,transaccion):
        vendedor = self.get_player_by_id(1)
        comprador = self.get_player_by_id(2)
        if (transaccion == 1):
            vendedor.payoff=c(self.precio_vendedor-self.costo_producto)
            comprador.payoff=c(self.valoracion_cpu-self.precio_vendedor)
        elif (transaccion==2):
            vendedor.payoff=c(self.costo_producto*(-1))
            comprador.payoff = c(0)
        else:
            vendedor.payoff = c(0)
            comprador.payoff = c(0)

class Player(BasePlayer):
    ganancias_totales= models.CurrencyField(initial=c(0))

    def role(self):
        if self.id_in_group == 1:
            return 'Vendedor'
        else:
            return 'Comprador'
