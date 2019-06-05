from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class presentacion(Page):
    def is_displayed(self):
        return self.round_number == 1

class tratamientos(Page):
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"]/2 +1

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"]
        }

class decision(Page):
    form_model = 'player'
    form_fields = ['da_invertir']

    """def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.round_number > self.session.config["Rounds"]/2
        else:
            return self.round_number <= self.session.config["Rounds"]/2"""

"""class loteria(Page):
    form_model = 'player'
    form_fields = ['da_invertir']

    def is_displayed(self):
        if (self.session.config["ConSin"]):
            return self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.round_number > self.session.config["Rounds"] / 2"""

class Ganancias(Page):
    pass

class GananciasTotal(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

class espera_grupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):
    def after_all_players_arrive(self):
        if (self.session.config["ConSin"]):
            if(self.round_number<= self.session.config["Rounds"]):
                self.subsession.seleccionar_ganador_loteria()
            else:
                self.subsession.seleccionar_ganador_subasta()
        else:
            if (self.round_number <= self.session.config["Rounds"]):
                self.subsession.seleccionar_ganador_subasta()
            else:
                self.subsession.seleccionar_ganador_loteria()
        jugadores=self.subsession.get_players()
        for i in jugadores:
            i.calcular_ganancia_ronda()
            i.calcular_ganancias_totales()

class precalculos(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.calcular_valores_productos()

class gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    precalculos,
    presentacion,
    tratamientos,
    espera_grupos,
    decision,
    espera_grupos,
    calculos,
    Ganancias,
    GananciasTotal,
    gracias
]
