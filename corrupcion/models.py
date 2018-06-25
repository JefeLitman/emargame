from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint
from random import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'corrupcion'
    players_per_group = 4
    num_rounds = 40
    cdp=c(50000)

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):

    aceptaC1 = models.BooleanField(initial=False,choices=[[True,'Si participa'],[False,'No participa']])
    aceptaC2 = models.BooleanField(initial=False,choices=[[True,'Si participa'],[False,'No participa']])
    aceptaC3 = models.BooleanField(initial=False,choices=[[True,'Si participa'],[False,'No participa']])

    def get_nivelxcp(self):
        contratistas = self.get_player_by_role("Burocrata").get_others_in_group()
        aceptados=[]
        for i in contratistas:
            if(i.aceptado==True):
                aceptados.append(i)
        if(len(aceptados)!=0):
            for i in aceptados:
                if (i.cuenta_publica == max([j.cuenta_publica for j in aceptados])):
                    i.ganador=True
                    self.get_player_by_role("Burocrata").cuenta_privada=i.soborno
                    return i.nivel_tecnologia*i.cuenta_publica/4
        else:
            return 0

    def set_niveles_tecnologia(self):
        contratistas=self.get_player_by_role("Burocrata").get_others_in_group()
        for i in contratistas:
            i.nivel_tecnologia=randint(1,3)+random()

    def set_aceptaciones(self):
        self.get_player_by_id(2).aceptado = self.aceptaC1
        self.get_player_by_id(3).aceptado = self.aceptaC2
        self.get_player_by_id(4).aceptado = self.aceptaC3

class Player(BasePlayer):
    cuenta_publica=models.CurrencyField(initial=c(0))
    cuenta_privada=models.CurrencyField(initial=c(0))
    nivel_tecnologia=models.FloatField()
    aceptado=models.BooleanField(initial=False)
    ganador=models.BooleanField(initial=False)
    soborno=models.CurrencyField(initial=c(0))
    ganancias_totales=models.CurrencyField(initial=c(0))

    def role(self):
        if(self.id_in_group == 1):
            return "Burocrata"
        else:
            return "Contratista"

    def set_payoff(self,nivelxcp):
        if (self.role()=="Burocrata"):
            self.payoff=self.cuenta_privada+nivelxcp
        elif(self.ganador==True):
            self.payoff = self.cuenta_privada + nivelxcp
        else:
            self.payoff = nivelxcp

    def set_ganancias_totales(self,max_rondas):
        ronda_aleatoria=random(1,max_rondas)
        self.ganancias_totales=self.in_round(ronda_aleatoria).payoff
        return ronda_aleatoria
