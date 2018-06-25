from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint

author = 'Luis Alejandro Palacio García & Daniel Felipe Parra Carreño'

doc = """
Tomando como referencia el diseño propuesto por Bergstrom y Miller (2000), este juego permite analizar, entender y discutir los efectos de la intervención del gobierno cuando prohíbe una transacción de mercado. La pregunta de investigación es: ¿Cómo afecta la prohibición de una transacción las decisiones de los compradores y los vendedores? Se evidencia cómo la prohibición por parte del gobierno de una transacción mutuamente beneficiosa lleva a los vendedores a aumentar el precio de mercado, disminuyendo el bienestar de los implicados.
<br/><br/>Bergstrom, T., & Miller, J. (2000). Experimentos con los principios económicos. Madrid: Antoni Bosh Editor.
"""

class Constants(BaseConstants):
    name_in_url = 'mercados_prohibidos'
    players_per_group = 2
    num_rounds = 20

class Subsession(BaseSubsession):
    Round_number=models.IntegerField(initial=0)
    Reinicio=models.BooleanField(initial=False)
    TSIN=models.BooleanField(initial=False)
    def creating_session(self):
        self.group_randomly()

class Group(BaseGroup):
    costo_producto=models.CurrencyField()
    valoracion_cpu=models.CurrencyField()
    precio_vendedor=models.CurrencyField()
    valoracion_comprador=models.CurrencyField()
    revision=models.IntegerField(initial=randint(1,100),blank=True)

    def set_payoff(self,transaccion):
        vendedor = self.get_player_by_id(1)
        comprador = self.get_player_by_id(2)
        if (transaccion == 1):
            vendedor.payoff=self.precio_vendedor-self.costo_producto
            comprador.payoff=self.valoracion_cpu-self.precio_vendedor
        elif (transaccion==2):
            vendedor.payoff=self.costo_producto*(-1)
            comprador.payoff = c(0)
        else:
            vendedor.payoff = c(0)
            comprador.payoff = c(0)

    def set_random_variables(self):
        self.costo_producto=c(randint(0,1000))
        self.valoracion_cpu=c(randint(1000,2000))

class Player(BasePlayer):
    ganancias_totales= models.CurrencyField(initial=c(0))

    def role(self):
        if self.id_in_group == 1:
            return 'Vendedor'
        else:
            return 'Comprador'

