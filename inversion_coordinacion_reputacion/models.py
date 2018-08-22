from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint

author = 'Luis Alejandro Palacio García & Laura Milena Prada Medina'

doc = """
Inspirados en el problema de alcanzar la eficiencia en juegos de coordinación abordado por Cooper, 
et al (1992), este juego permite analizar, entender y discutir el efecto de la reputación sobre 
una decisión de inversión en un contexto de negociación bilateral. 
Las preguntas que se busca discutir son:<br>
<br>¿Cómo afecta la reputación las decisiones de inversión que requieren de coordinación?
<br>¿El mecanismo de calificación es una señal efectiva?
<br>Se espera que los estudiantes discutan si el mecanismo de calificación permite señalizar 
el comportamiento prosocial, mejorando la coordinación y por la tanto la eficiencia.
<br><br>Cooper, R., DeJong, D., Forsythe, R., y Ross, T. (1992). Communication in coordination games. 
Quarterly Journal of Economics, 107(2), 739–771.
"""


class Constants(BaseConstants):
    name_in_url = 'inversion_coordinacion_reputacion'
    players_per_group = 2
    num_rounds = 30
    Dotacion=c(1000)


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
    Rentabilidad=models.CurrencyField()
    def calcular_gananancia(self,p1inversion,p2inversion):
            self.Rentabilidad=p1inversion*p2inversion/500
            return self.Rentabilidad


class Player(BasePlayer):
    Codigo = models.StringField()
    Inversion=models.CurrencyField(blank=True,min=c(0),max=c(1000))
    Calificacion=models.IntegerField(blank=True, min=1, max=5)
    Reputacion=models.FloatField()
    Pagos = models.CurrencyField(initial=c(0))
    TotalPagos = models.CurrencyField(initial=c(0))

    def set_inversion_azar(self):
        self.Inversion=randint(0,1000)

    def set_calificacion_azar(self,ronda, rondas_totales, consin):
        if (consin):
            if (ronda <= rondas_totales / 2): #Calculo de califiacion azar cuando es de con a sin
                self.Calificacion = randint(1, 5)
        else:
            if (ronda > rondas_totales / 2):
                self.Calificacion = randint(1, 5)

    def set_reputacion(self,ronda, rondas_totales, consin):
        if (consin):
            if (ronda <= rondas_totales / 2): #Calculo de reputacion cuando es de con a sin
                self.Reputacion = sum(
                    [p.Calificacion for p in self.in_rounds(1, ronda)]) / ronda
        else:
            if (ronda == rondas_totales / 2): #Calculo de reputacion cuando es de sin a con
                self.Reputacion = 5
            elif (ronda > rondas_totales / 2):
                self.Reputacion = sum([p.Calificacion for p in self.in_rounds(rondas_totales / 2 + 1, ronda)]) / (
                            ronda - rondas_totales / 2)

    def set_pago(self,ganancia_grupo):
        self.Pagos=Constants.Dotacion-self.Inversion+ganancia_grupo
        self.payoff=self.Pagos

    def set_totalpagos(self):
        self.TotalPagos=sum([p.Pagos for p in self.in_all_rounds()])