from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instrucciones(Page):
    pass

class Conocimientos(Page):
    #timeout_seconds = 10
    form_model = 'player'
    form_fields = ['I1AG','I1AO','I1BG','I1BO']

class Argumentacion(Page):
    #timeout_seconds = 10
    form_model = 'player'
    form_fields = ['I2AG','I2AO','I2BG','I2BO']

class Discusion(Page):
    #timeout_seconds = 10
    form_model = 'player'
    form_fields = ['I3AG','I3AO','I3BG','I3BO']

class General(Page):
    #timeout_seconds = 10
    form_model = 'player'
    form_fields = ['I1G','I2G','I3G','I4G']

class esperaTodosJugadores(WaitPage):
    wait_for_all_groups = True

class Calculos(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.calculopromIAG()
        self.subsession.calculopromIAO()
        self.subsession.calculopromIBG()
        self.subsession.calculopromIBO()
        self.subsession.calculopromIG()


class Resultados(Page):
    def vars_for_template(self):
        return {
            'PromAG': self.subsession.calcularCasaGanadora()[0],
            'PromAO': self.subsession.calcularCasaGanadora()[1],
            'PromBG': self.subsession.calcularCasaGanadora()[2],
            'PromBO': self.subsession.calcularCasaGanadora()[3]
        }


class Ganador(Page):
    def vars_for_template(self):
        return {
            'DebateGeneral': self.subsession.calcularDebateGeneral()
        }

class Gracias(Page):
    #Tambien ponemos? timeout_seconds = 30
    pass


page_sequence = [
    Instrucciones,
    Conocimientos,
    Argumentacion,
    Discusion,
    General,
    esperaTodosJugadores,
    Calculos,
    Resultados,
    Ganador,
    Gracias,
]

