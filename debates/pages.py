from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Presentacion(Page):
    pass

class Equipo(Page):
    #timeout_seconds = 5
    form_model = 'player'
    form_fields = ['I1AF','I1EC']

class Conocimiento(Page):
    #timeout_seconds = 5
    form_model = 'player'
    form_fields = ['I2AF','I2EC']

class Coherencia(Page):
    #timeout_seconds = 5
    form_model = 'player'
    form_fields = ['I3AF','I3EC']

class Vocabulario(Page):
    #timeout_seconds = 5
    form_model = 'player'
    form_fields = ['I4AF','I4EC']

class Escucha(Page):
    #timeout_seconds = 5
    form_model = 'player'
    form_fields = ['I5AF','I5EC']

class esperaTodosJugadores(WaitPage):
    wait_for_all_groups = True

class Calculos(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.calculopromIAF()
        self.subsession.calculopromIEC()

class Resultados(Page):
    # Tambien ponemos? timeout_seconds = 60
    pass

class Ganador(Page):
    def vars_for_template(self):
        return {
           'CasaAFavor': self.subsession.calcularCasaGanadora()[0],
           'CasaEnContra': self.subsession.calcularCasaGanadora()[1]
        }

class Gracias(Page):
    #Tambien ponemos? timeout_seconds = 30
    pass


page_sequence = [
    Presentacion,
    Equipo,
    Conocimiento,
    Coherencia,
    Vocabulario,
    Escucha,
    esperaTodosJugadores,
    Calculos,
    Resultados,
    Ganador,
    Gracias,
]
