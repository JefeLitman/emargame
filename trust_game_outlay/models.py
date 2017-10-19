from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Luis Alejandro Palacio Garcia & Laura Milena Prada Medina & Mayra Alejandra Riascos Diaz & Edgar Yesid Rangel Pieschacon'

doc = """
Los juegos de negociación son un ejercicio pedagógico que aumenta el interés de los estudiantes en la teoría económica, utilizando como metodología la economía experimental. Este trabajo tiene como objetivo diseñar y validar un protocolo experimental que permita analizar, entender y discutir cómo afecta una etiqueta de grupo la confianza y la reciprocidad en los que comparten la misma característica y los que no. En particular, los participantes auto reportarán si son hombre o mujer para ver si esta información sobre la pareja afecta las decisiones. La pregunta de investigación es: ¿Cómo afecta la confianza y la reciprocidad el hecho de conocer si la pareja es hombre o mujer? ¿El comportamiento de hombres y mujeres es diferente, o cambia en función de si estoy interactuando con alguien igual o diferente? Para evocar una mayor identificación con el grupo, en todos los periodos se informará los puntos promedio que han ganado los hombres y las mujeres. Se espera que la información sobre la pareja aumente la confianza y la reciprocidad entre los iguales, dado que el sentimiento de pertenencia se refuerza por la comparación del desempeño promedio.
"""


class Constants(BaseConstants):
    name_in_url = 'trust_game_outlay'
    players_per_group = 2
    num_rounds = 2

    endowment = c(1000)
    multiplication_factor = 3


class Subsession(BaseSubsession):
    gananciamujeres=models.CurrencyField(initial=c(0))
    gananciahombres=models.CurrencyField(initial=c(0))

    def set_ganmujer(self):
        


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        choices=currency_range(0,Constants.endowment,c(1)),
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
    genre=models.PositiveIntegerField(
        choices=[
            [1,'Mujer'],
            [2, 'Hombre'],
        ],
        initial=0
    )
    gananciajugador=models.CurrencyField(initial=c(0))

    def get_genre(self):
        return self.genre

    def set_gananciajugador(self,valor):
        self.gananciajugador=valor
