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
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    genre=models.PositiveIntegerField(
        choices=[
            [1,'Mujer'],
            [2, 'Hombre'],
        ]
    )
