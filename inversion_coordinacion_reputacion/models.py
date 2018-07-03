from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


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

    pago=c(1000)


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    def calcular_gananancia(self,p1inversion,p2inversion):
            ganancia=p1inversion*p2inversion/500
            return ganancia


class Player(BasePlayer):
    inversion=models.CurrencyField(initial=c(0),min=c(0),max=c(1000))
    calificacion=models.IntegerField(initial=0, min=1, max=5)
    calificacion_promedio=models.FloatField(initial=0,min=1,max=5)
    ganancia_total = models.CurrencyField(initial=c(0))

    def set_payoff(self,ganancia):
        self.payoff=Constants.pago-self.inversion+ganancia

    def get_calificacion(self,nota):
        return self.calificacion

    def get_ganancias(self):
        return self.ganancia_total

    def get_companero(self):
        return self.get_others_in_group()[0]