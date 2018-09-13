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

    def get_azul_promedio(self):
        jugadores=self.get_players()
        ganancia_promedio = 0
        for p in jugadores:
            if p.Azul == 1:
                ganancia_promedio = ganancia_promedio + p.payoff
        ganancia_promedio = ganancia_promedio / (len(jugadores) / 2)
        return ganancia_promedio

    def get_verde_promedio(self):
        jugadores = self.get_players()
        ganancia_promedio = 0
        for p in jugadores:
            if p.Azul == 0:
                ganancia_promedio = ganancia_promedio + p.payoff
        ganancia_promedio = ganancia_promedio / (len(jugadores) / 2)
        return ganancia_promedio

    def creating_session(self):
        self.group_randomly(fixed_id_in_group=True)

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Participante_A = models.BooleanField()
    Azul = models.BooleanField(
        choices=[
            [True, 'Azul'],
            [False, 'Verde']
        ]
    )
    Recibe = models.CurrencyField()
    Envia = models.CurrencyField(blank=True,min=c(0))
    Pagos = models.CurrencyField(initial=c(0))
    TotalPagos = models.CurrencyField(initial=c(0))
    Codigo = models.StringField()

    def set_participantes(self,es_la_mitad):
        if es_la_mitad == True:
            if self.id_in_group == 1:
                self.Participante_A=True
            else:
                self.Participante_A = False
        else:
            if self.id_in_group == 1:
                self.Participante_A = True
            else:
                self.Participante_A = False

    def set_colores(self,RondasTotales):
        for p in self.in_rounds(2,RondasTotales):
            p.Azul = p.in_round(1).Azul

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