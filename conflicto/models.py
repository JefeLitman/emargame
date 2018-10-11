from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint
author = 'Luis Alejandro Palacio García & Ismael Estrada Cañas & Carolina Andrea Estévez Fiallo'

doc = """
Adaptando el modelo propuesto por Palacio, Cortés y Muñoz-Herrera (2015), este juego permite analizar, 
entender y discutir el efecto del nivel de conflicto y los mensajes vinculantes sobre la decisión 
de cooperar en juegos 2×2. Las preguntas de investigación son:<br>
<br>¿Los participantes están más dispuestos a cooperar dependiendo del nivel de conflicto al 
que se enfrenten?
<br>¿El hecho de jugar de forma secuencial lleva a cooperar más que cuando se juega simultáneamente?
<br>Se espera que el nivel de conflicto afecte la decisión de cooperar. Entre mayor sea el conflicto, 
mayores incentivos tienen los participantes para actuar agresivamente. Con respecto al comportamiento 
del líder o del seguidor, no se espera cambios significativos con respecto al juego simultáneo.
<br><br>Palacio, L., Cortés, A., & Muñoz-Herrera, M. (2015). The strategic role of nonbinding 
communication. Applied Mathematics, 2015, 11.
"""

class Constants(BaseConstants):
    name_in_url = 'conflicto'
    players_per_group = 2
    num_rounds = 20


class Subsession(BaseSubsession):
    Reinicio = models.BooleanField()
    TSEC = models.BooleanField()

    def set_variables_subsesion(self, ronda, rondas_totales, secsim):
        self.Reinicio = ronda > rondas_totales / 2
        if (secsim):
            if (ronda <= rondas_totales / 2):
                self.TSEC = True
            else:
                self.TSEC = False
        else:
            if (ronda <= rondas_totales / 2):
                self.TSEC = False
            else:
                self.TSEC = True

    def creating_session(self):
        if (self.round_number <= self.session.config["Rounds"]):
            self.set_variables_subsesion(self.round_number,self.session.config["Rounds"],self.session.config["SecSim"])
            self.group_randomly()
            for g in self.get_groups():
                g.set_variables()
                g.get_player_by_id(1).Participante_Azul = True
                g.get_player_by_id(2).Participante_Azul = False

class Group(BaseGroup):
    VariableX=models.IntegerField()
    VariableY=models.IntegerField()

    def set_variables(self):
        self.VariableX=randint(0,500)
        self.VariableY=randint(500,1500)

class Player(BasePlayer):
    Eleccion = models.IntegerField(blank=True)
    Participante_Azul = models.BooleanField()
    Pagos=models.CurrencyField(initial=c(0))
    TotalPagos = models.CurrencyField(initial=c(0))
    Codigo = models.StringField()

    def role(self):
        if self.Participante_Azul == True:
            return 'Azul'
        else:
            return 'Verde'

    def set_eleccion_azar(self):
        self.Eleccion = randint(1,2)

    def set_pagos(self):
        if self.Participante_Azul == True:
            matrix = [[c(1000), c(self.group.VariableX)], [c(self.group.VariableY), c(250)]]
            self.Pagos = matrix[self.Eleccion-1][self.get_others_in_group()[0].Eleccion-1]
        else:
            matrix = [[c(1000), c(self.group.VariableY)], [c(self.group.VariableX), c(250)]]
            self.Pagos = matrix[self.get_others_in_group()[0].Eleccion - 1][self.Eleccion - 1]
        self.payoff = self.Pagos

    def set_totalpagos(self):
        self.TotalPagos = sum([p.Pagos for p in self.in_all_rounds()])