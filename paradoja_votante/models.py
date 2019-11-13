from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint
from random import random
from sklearn.preprocessing import MinMaxScaler


author = 'Luis Alejandro Palacio García & Ferley Rincon'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'paradoja_votante'
    players_per_group = None
    num_rounds = 20
    Costo = c(500)
    Multiplicador = c(500)

class Subsession(BaseSubsession):
    Reinicio = models.BooleanField()
    TSIN =  models.BooleanField()
    N_Azules = models.FloatField()
    N_Rojos = models.FloatField()
    N_Verdes = models.FloatField()
    V_Azul = models.IntegerField()
    V_Rojo = models.IntegerField()
    V_Verde = models.IntegerField()
    Ganador = models.StringField()

    def creating_session(self):
        self.set_preferencias_jugadores()
        self.set_n_jugadores()

    def set_variables_subsesion(self, ronda, rondas_totales, ConSin):
        # Definiendo la variable de reinicio
        self.Reinicio = ronda > rondas_totales / 2
        # Definiendo la variable de TMAS
        if (ConSin):
            if (ronda <= rondas_totales / 2):
                self.TSIN = False
            else:
                self.TSIN = True
        else:
            if (ronda <= rondas_totales / 2):
                self.TSIN = True
            else:
                self.TSIN = False

    def set_preferencias_jugadores(self):

        for j in self.get_players():
            Preferencias = [1,2,3]
            j.P_Azul = Preferencias.pop(randint(0,len(Preferencias)-1))
            j.P_Rojo = Preferencias.pop(randint(0,len(Preferencias)-1))
            j.P_Verde = Preferencias[0]

    def set_n_jugadores(self):
        """obtener la distribución de cada partido"""
        contA, contR, contV,contNo = 0, 0, 0, 0
        l = len(self.get_players())
        for j in self.get_players():
            if j.P_Azul == 3:
                contA = contA + 1
            elif j.P_Rojo == 3:
                contR = contR + 1
            else:
                contV = contV + 1
        self.N_Azules = 100*float("{0:.2f}".format(contA/l))
        self.N_Verdes = 100*float("{0:.2f}".format(contV/l))
        self.N_Rojos = 100*float("{0:.2f}".format(contR/l))

    def get_distribucion_preferencias(self):
        distribucion_preferencias = {'Azul':self.N_Azules, 'Verde': self.N_Verdes, 'Rojo': self.N_Rojos}
        Valores = list(distribucion_preferencias.values())
        Valores.sort(reverse=True)
        Llaves = list(distribucion_preferencias.keys())
        orden_candidatos = []
        for v in Valores:
            for l in Llaves:
                if v == distribucion_preferencias.get(l):
                    orden_candidatos.append(l)
        preferencias = [orden_candidatos,Valores]
        return preferencias

    def set_ganador(self):
        contA, contR, contV,contVN = 0, 0, 0,0
        for j in self.get_players():
            if j.Voto_Azul == True:
                contA = contA + 1
            elif j.Voto_Rojo == True:
                contR = contR + 1
            elif j.Voto_Verde == True:
                contV = contV + 1
            else:
                contVN = contVN+1
        Votos = {"Azul":contA + random(),"Verde":contV + random(),"Rojo":contR + random()}
        Valores = list(Votos.values())
        Valores.sort()
        Llaves = list(Votos.keys())
        for v in Valores:
            for l in Llaves:
                if v == Votos.get(l):
                    self.Ganador = l

    def getPagosTotalesJugadores(self):
        jugadores = self.get_players()
        PagosTotalesJugadores = []
        for j in jugadores:
            PagosTotalesJugadores.append([j.TotalPagos])
        return PagosTotalesJugadores

    def getPuntajesCalificaciones(self):
        Puntajes = self.getPagosTotalesJugadores()
        scaler = MinMaxScaler(feature_range=(30, 50))
        Calificaciones = scaler.fit_transform(Puntajes)

        return Calificaciones

    def setNotas(self):
        jugadores = self.get_players()
        calificaciones = self.getPuntajesCalificaciones()
        for j in range(len(jugadores)):
            jugadores[j].Calificacion = calificaciones[j]


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Codigo = models.StringField()

    P_Azul = models.IntegerField(min=1, max=3)
    P_Rojo = models.IntegerField(min=1, max=3)
    P_Verde = models.IntegerField(min=1, max=3)

    Voto_Azul = models.BooleanField(blank=True)
    Voto_Rojo = models.BooleanField(blank=True)
    Voto_Verde = models.BooleanField(blank=True)
    VotoNo = models.BooleanField(blank=True)

    Pagos = models.CurrencyField(min=0, max=1500)
    TotalPagos = models.CurrencyField()
    Preferencia_ganador = models.IntegerField(min=1, max=3)

    Calificacion = models.FloatField()

    def setPagos(self):
        self.Pagos = self.Preferencia_ganador * Constants.Multiplicador - Constants.Costo * c(not self.VotoNo)
        self.payoff = self.Pagos

    def setTotalPagos(self):
        #La suma de todos los pagos en todas las rondas
        self.TotalPagos = sum([p.Pagos for p in self.in_all_rounds()])

    def get_orden_preferencias(self):
        Candidatos = {'Azul':self.P_Azul ,'Rojo':self.P_Rojo,'Verde':self.P_Verde}
        Valores = list(Candidatos.values())
        Valores.sort(reverse=True)
        Llaves = list(Candidatos.keys())
        orden_candidatos = []
        for v in Valores:
            for l in Llaves:
                if v == Candidatos.get(l):
                    orden_candidatos.append(l)
        return orden_candidatos

    def set_preferencia_ganador(self, ganador):
        Candidatos = {'Azul':self.P_Azul ,'Rojo':self.P_Rojo,'Verde':self.P_Verde}
        self.Preferencia_ganador = Candidatos.get(ganador)

    def set_votacion_aleatorio(self):
        votos = [self.Voto_Azul,self.Voto_Rojo,self.Voto_Verde,self.VotoNo]
        if True in votos:
            self.set_false()
        else:
            posicion_true = randint(0, len(votos) - 1)
            votos[posicion_true] = True
            if posicion_true == 0:
                self.Voto_Azul = True
            elif posicion_true == 1:
                self.Voto_Rojo = True
            elif posicion_true == 2:
                self.P_Verde = True
            else:
                self.VotoNo = True
            self.set_false()

    def set_false(self):
        if self.Voto_Azul == None:
            self.Voto_Azul = False
        if self.Voto_Rojo == None:
            self.Voto_Rojo = False
        if self.Voto_Verde == None:
            self.Voto_Verde = False
        if self.VotoNo == None:
            self.VotoNo = False




