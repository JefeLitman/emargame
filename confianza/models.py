from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint

author = 'Luis Alejandro Palacio Garcia & Laura Milena Prada Medina'

doc = """
Retomando la literatura relacionada con el juego de la confianza clásico propuesto por Berg, 
Dickhaut, y McCabe (1995), este juego permite analizar, entender y discutir el efecto de una 
etiqueta de grupo sobre la confianza y la reciprocidad en los que comparten la misma característica 
y los que no. En particular, los participantes auto reportarán si son hombre o mujer para ver 
si esta información sobre la pareja afecta las decisiones. La pregunta de investigación es:<br>
<br>¿Cómo afecta la confianza y la reciprocidad el hecho de conocer si la pareja es hombre o mujer?
<br>¿El comportamiento de hombres y mujeres es diferente, o cambia en función de si estoy 
interactuando con alguien igual o diferente?
<br>Se espera que la información sobre la pareja aumente la confianza y la reciprocidad entre 
los iguales, dado que el sentimiento de pertenencia se refuerza por la comparación del desempeño 
promedio.
<br><br>Berg, J., Dickhaut, J., y McCabe, K. (1995). Trust, reciprocity, and social history. 
Games and Economic Behavior, 10, 122–142.
"""

class Constants(BaseConstants):
    name_in_url = 'trust_game_outlay'
    players_per_group = 2
    num_rounds=20
    Dotacion = c(1000)
    Multiplicador = 3


class Subsession(BaseSubsession):
    Reinicio = models.BooleanField()
    TSIN = models.BooleanField()
    Ganancia_Promedio_Azul=models.CurrencyField(initial=c(0))
    Ganancia_Promedio_Verde=models.CurrencyField(initial=c(0))

    def set_variables_subsesion(self, ronda, rondas_totales, consin):
        self.Reinicio = ronda > rondas_totales / 2
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

    def set_ganancias_promedios(self,azules,verdes):
        if len(azules) != 0:
            self.Ganancia_Promedio_Azul = sum([p.payoff for p in azules])/len(azules)
        if len(verdes) != 0:
            self.Ganancia_Promedio_Verde = sum([p.payoff for p in verdes])/len(verdes)

    def creating_session(self):
        self.group_randomly()

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Participante_A = models.BooleanField()
    Azul = models.BooleanField()
    Recibe = models.CurrencyField()
    Envia = models.CurrencyField(blank=True,min=c(0),max=c(1000))
    Pagos = models.CurrencyField(initial=c(0))
    TotalPagos = models.CurrencyField(initial=c(0))

    def set_participantes(self):
        self.Participante_A = randint(0,1)
        self.Azul = randint(0,1)

    def role(self):
        if self.Azul == 1:
            return 'Azul'
        else:
            return 'Verde'

    def set_envia_azar(self):
        self.Envia = randint(0,1000)
    
    def set_pagos(self):
        if self.Participante_A == 1:
            self.Pagos = Constants.Dotacion - self.Envia + self.Recibe
        else:
            self.Pagos = Constants.Multiplicador*self.Recibe - self.Envia
        self.payoff = self.Pagos

    def set_totalpagos(self):
        self.TotalPagos = sum([p.Pagos for p in self.in_all_rounds()])