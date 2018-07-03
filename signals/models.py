from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Luis Alejandro Palacio García & Ismael Estrada Cañas & Bryan Snehider Díaz'

doc = """
Como una ampliación del juego propuesto por Palacio, Saravia y Vesga (2017), este juego permite 
analizar, entender y discutir hasta qué punto los bienes de buena calidad pueden ser expulsados 
del mercado cuando los vendedores no logran transmitir de forma creíble su información privada. 
Las preguntas de investigación son:<br>
<br>¿Los vendedores están dispuestos a invertir recursos para comunicar la calidad del bien a transar?
<br>¿El mecanismo de señales permite solucionar el problema de selección adversa?
<br>Se espera que en ausencia de compromiso los participantes tengan incentivos a mentir, lo que 
lleva al colapso del mercado. En cambio, cuando se puede invertir recursos para comunicar la 
verdadera calidad, las señales vinculantes ayudan a alcanzar un equilibrio socialmente deseable.
<br><br>Palacio, L., Saravia, I., & Vesga, M. (2017). Juegos en el salón de clase: 
El mercado de los limones. Revista de Economia Institucional, 19(36), 291–311.354
"""


class Constants(BaseConstants):
    name_in_url = 'signals'
    players_per_group = 2
    num_rounds = 30
    valor = [c(500), c(1000), c(1500), c(2000), c(2500)]
    costo = [c(100), c(200), c(300), c(400), c(500)]


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    calidad_real=models.IntegerField(initial=1,min=1,max=5)
    calidad_ofrecida=models.IntegerField(initial=1,min=1,max=5)
    precio_vendedor=models.CurrencyField(initial=c(0),min=c(0),max=c(2500)) #Valor(precio)
    decision_comprador=models.BooleanField(initial=False,choices=[
        [True,'Si'],
        [False,'No']
    ],widget=widgets.RadioSelect)

    decision_vendedor = models.BooleanField(initial=False, choices=[
        [True, 'Si'],
        [False, 'No']
    ],widget=widgets.RadioSelect)

    def set_payoffs(self):
        vendedor=self.get_player_by_id(1)
        comprador=self.get_player_by_id(2)
        if(self.decision_comprador): #(si lo compra, el comprador?)
            comprador.payoff=Constants.valor[self.calidad_real-1]-self.precio_vendedor
            if(self.decision_vendedor): #(si el vendedor toma la decision de invertir los 500 pts)
                vendedor.payoff=self.precio_vendedor-Constants.costo[self.calidad_real-1]-c(500)
            else:
                vendedor.payoff = self.precio_vendedor - Constants.costo[self.calidad_real - 1]
        else:
            vendedor.payoff=c(0)
            comprador.payoff=c(0)

class Player(BasePlayer):
    ganancias_totales=models.CurrencyField(initial=c(0))

    def role(self):
        if self.id_in_group == 1:
            return 'Vendedor'
        if self.id_in_group == 2:
            return 'Comprador'
