from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


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
    num_rounds=30
    endowment = c(1000)
    multiplication_factor = 3


class Subsession(BaseSubsession):
    gananciamujeres=models.CurrencyField(initial=c(0))
    gananciahombres=models.CurrencyField(initial=c(0))

    def set_ganancias(self,mujeres,hombres):
        if len(mujeres) != 0:
            self.gananciamujeres = sum([p.payoff for p in mujeres])/len(mujeres)
        if len(hombres) != 0:
            self.gananciahombres = sum([p.payoff for p in hombres])/len(hombres)

    def creating_session(self):
        self.group_randomly()

class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        min=c(0),max=c(1000),
        initial=c(0)
    )
    sent_back_amount = models.CurrencyField(
        initial=c(0)
    )

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount

class Player(BasePlayer):
    Codigo = models.StringField()
    genre=models.StringField(
        choices=[
            'Inventor',
            'Inversor',
        ]
    )
    gananciajugador=models.CurrencyField(initial=c(0))

    def get_genre(self):
        return self.genre

    def set_gananciajugador(self,valor):
        self.gananciajugador=valor

    def role(self):
        return self.in_round(1).genre
