from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint

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
    num_rounds = 20
    Valores = [c(500), c(1000), c(1500), c(2000), c(2500)]
    Costos = [c(100), c(200), c(300), c(400), c(500)]

class Subsession(BaseSubsession):
    Reinicio = models.BooleanField()
    TSIN = models.BooleanField()
    def set_variables_subsesion(self, ronda, rondas_totales, consin):
        # Definiendo la variable de reinicio
        self.Reinicio = ronda > rondas_totales / 2
        # Definiendo la variable de TSIN
        if (consin):
            if (ronda <= rondas_totales / 2):
                self.TSIN = False
            else:
                self.TSIN = True
        else:
            if (ronda <= rondas_totales / 2):
                self.TSIN = True
            else:
                self.TSIN = False
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    Costo=models.CurrencyField()
    Valor=models.CurrencyField()
    Calidad=models.IntegerField(blank=True,min=1,max=5)
    Mensaje=models.IntegerField(blank=True,min=1,max=5)
    Senal = models.BooleanField(blank=True, choices=[
        [True, 'Si'],
        [False, 'No']
    ])
    Precio=models.CurrencyField(blank=True,min=c(0),max=c(2500))
    Transaccion=models.BooleanField(blank=True,choices=[
        [True,'Si'],
        [False,'No']
    ])

    def set_pagos(self):
        vendedor=self.get_player_by_id(1)
        comprador=self.get_player_by_id(2)
        if(self.Transaccion): #(si lo compra, el comprador)
            comprador.Pagos=Constants.Valores[self.Calidad-1]-self.Precio
            if(self.Senal): #(si el vendedor toma la decision de invertir los 500 pts)
                vendedor.Pagos=self.Precio-Constants.Costos[self.Calidad-1]-c(500)
            else:
                vendedor.Pagos = self.Precio - Constants.Costos[self.Calidad - 1]
        else:
            vendedor.Pagos=c(0)
            comprador.Pagos=c(0)
        vendedor.payoff=vendedor.Pagos #En esta parte se igualan los payoffs a pagos
        comprador.payoff=comprador.Pagos
        vendedor.set_totalpagos()#En esta parte se hace el calculo de los pagos totales en la ronda
        comprador.set_totalpagos()

    def set_costo_valor(self):
        self.Costo=Constants.Costos[self.Calidad-1]
        self.Valor=Constants.Valores[self.Calidad-1]

    def set_calidad_azar(self):
        self.Calidad = randint(1, 5)

    def set_mensaje_azar(self):
        self.Mensaje = randint(1, 5)

    def set_precio_azar(self):
        self.Precio = randint(Constants.Costos[self.Calidad - 1], 2500)

    def set_senal_azar(self,ronda,rondas_totales,consin):
        if (consin):
            if (ronda <= rondas_totales / 2):
                self.Senal= randint(0,1)
                if(self.Senal):
                    self.Mensaje=self.Calidad
        else:
            if (ronda > rondas_totales / 2):
                self.Senal= randint(0,1)
                if (self.Senal):
                    self.Mensaje = self.Calidad

    def set_transaccion_azar(self):
        self.Transaccion= randint(0,1)

class Player(BasePlayer):
    Pagos=models.CurrencyField(initial=c(0))
    TotalPagos=models.CurrencyField(initial=c(0))
    Vendedor=models.BooleanField()

    def set_vendedor(self):
        if self.id_in_group == 1:
            self.Vendedor=True
        else:
            self.Vendedor=False

    def set_totalpagos(self):
        self.TotalPagos=sum([p.Pagos for p in self.in_all_rounds()])