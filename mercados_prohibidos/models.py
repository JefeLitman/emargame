from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint

author = 'Luis Alejandro Palacio García & Daniel Felipe Parra Carreño'

doc = """
Tomando como referencia el diseño propuesto por Bergstrom y Miller (2000), 
este juego permite analizar, entender y discutir los efectos de la intervención del gobierno 
cuando prohíbe una transacción de mercado. La pregunta de investigación es:<br>
<br>¿Cómo afecta la prohibición de una transacción las decisiones de los compradores y los vendedores?
<br>Se evidencia cómo la prohibición por parte del gobierno de una transacción mutuamente beneficiosa 
lleva a los vendedores a aumentar el precio de mercado, disminuyendo el bienestar de los implicados.
<br/><br/>Bergstrom, T., & Miller, J. (2000). Experimentos con los principios económicos. 
Madrid: Antoni Bosh Editor.
"""

class Constants(BaseConstants):
    name_in_url = 'mercados_prohibidos'
    players_per_group = 2
    num_rounds = 20

class Subsession(BaseSubsession):
    Reinicio=models.BooleanField()
    TSIN=models.BooleanField()
    def set_variables_subsesion(self,ronda,rondas_totales,consin):
        #Definiendo la variable de reinicio
        self.Reinicio = ronda > rondas_totales / 2
        # Definiendo la variable de TSIN
        if (consin):
            if (ronda <= rondas_totales/2):
                self.TSIN= False
            else:
                self.TSIN = True
        else:
            if (ronda <= rondas_totales/2):
                self.TSIN = True
            else:
                self.TSIN = False
    def creating_session(self):
        self.group_randomly()

class Group(BaseGroup):
    Costo=models.CurrencyField()
    Valor=models.CurrencyField()
    Precio=models.CurrencyField(blank=True)
    MPDA=models.CurrencyField(blank=True)
    RRevision=models.IntegerField()
    Revision=models.BooleanField()

    def set_pagos(self,transaccion):
        vendedor = self.get_player_by_id(1)
        comprador = self.get_player_by_id(2)
        if (transaccion == 1): #1 corresponde a que se realizo la transaccion sin revisarlo
            self.Revision = False
            vendedor.Pagos=self.Precio-self.Costo
            comprador.Pagos=self.Valor-self.Precio
        elif (transaccion == 2):#2 corresponde a que no se realizo la transaccion porque se reviso
            self.Revision=True
            vendedor.Pagos=self.Costo*(-1)
            comprador.Pagos = c(0)
        else: #Este seria el caso 3 donde no se realizo la transaccion porque no cumplio
            self.Revision = False
            vendedor.Pagos = c(0)
            comprador.Pagos = c(0)
        vendedor.payoff=vendedor.Pagos
        comprador.payoff=comprador.Pagos

    def set_variables_azar(self):
        self.RRevision=randint(1,100)
        self.Costo=c(randint(0,1000))
        self.Valor=c(randint(1000,2000))

class Player(BasePlayer):
    Pagos=models.CurrencyField(initial=c(0))
    TotalPagos= models.CurrencyField(initial=c(0))
    Vendedor=models.BooleanField()

    def set_vendedor(self):
        if self.id_in_group == 1:
            self.Vendedor=True
        else:
            self.Vendedor=False

    def set_totalpagos(self):
        self.TotalPagos=sum([p.Pagos for p in self.in_all_rounds()])