from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint


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
        contA, contR, contV,contNo = 0, 0, 0, 0
        l = len(self.get_players())
        for j in self.get_players():
            if j.P_AZul == 3:
                contA = contA + 1
            elif j.P_Rojo == 3:
                contR = contR + 1
            else:
                contV = contV + 1
        self.N_Azules = contA/l
        self.N_Verdes = contV/l
        self.N_Rojos = contR/l

        distribucion_preferencias = {'Azul':self.N_Azules, 'Verde': self.N_Verdes, 'Rojos': self.N_Rojos}
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
        Votos = {"Azul":contA,"Verdes":contV,"Rojos":contR,"No votaron": contVN}
        Valores = list(Votos.values())
        Valores.sort()
        Llaves = list(Votos.keys())
        for v in Valores:
            for l in Llaves:
                if v == Votos.get(l):
                    self.Ganador = l

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Codigo = models.StringField(min=1, max=3)

    P_Azul = models.IntegerField(min=1, max=3)
    P_Rojo = models.IntegerField(min=1, max=3)
    P_Verde = models.IntegerField(min=1, max=3)

    Voto_Azul = models.BooleanField()
    Voto_Rojo = models.BooleanField()
    Voto_Verde = models.BooleanField()
    VotoNo = models.BooleanField()

    Pagos = models.CurrencyField(min=0, max=1500)
    TotalPagos = models.CurrencyField()
    Preferencia_ganador = 0 #faltaaaaaa

    def setPagos(self):
        self.Pagos = self.Preferencia_ganador * Constants.Multiplicador - Constants.Costo * c(self.VotoNo)
        self.payoff = self.Pagos

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





