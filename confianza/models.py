from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint
from sklearn.preprocessing import MinMaxScaler

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

    def creating_session(self):
        if(self.round_number <= self.session.config["Rounds"]):
            jugadores=self.get_players()
            for i in range(0,len(jugadores)):
                if(self.round_number == 1):
                    if(i < len(jugadores)/2):
                        jugadores[i].Azul = True
                    else:
                        jugadores[i].Azul = False
                else:
                    jugadores[i].Azul=jugadores[i].in_round(1).Azul
            self.group_randomly()

    def get_total_azul(self):
        jugadores = self.get_players()
        total_azul = 0
        for p in jugadores:
            if p.Azul == 1:
                total_azul = total_azul + p.payoff
        return total_azul

    def get_total_verde(self):
        jugadores = self.get_players()
        total_verde = 0
        for p in jugadores:
            if p.Azul == 0:
                total_verde = total_verde + p.payoff
        return total_verde

    def getPagosTotalesJugadores(self):
        jugadores = self.get_players()
        PagosTotalesJugadores = []
        for j in jugadores:
            PagosTotalesJugadores.append([j.TotalPagos])
        return PagosTotalesJugadores

    def getPuntajesCalificaciones(self):
        Puntajes = self.getPagosTotalesJugadores()
        scaler = MinMaxScaler(feature_range=(3.0, 5.0))
        Calificaciones = scaler.fit_transform(Puntajes)

        return Calificaciones

    def setNotas(self):
        jugadores = self.get_players()
        calificaciones = self.getPuntajesCalificaciones()
        for j in range(len(jugadores)):
            jugadores[j].nota = calificaciones[j]


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Participante_A = models.BooleanField()
    Azul = models.BooleanField()
    Recibe = models.CurrencyField()
    Envia = models.CurrencyField(blank=True,min=c(0))
    Pagos = models.CurrencyField()
    TotalPagos = models.CurrencyField()
    Codigo = models.StringField()
    nota = models.FloatField()

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