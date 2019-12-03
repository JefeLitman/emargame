from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class presentacion(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1

class tratamientos(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"]/2 +1

    def vars_for_template(self):
        return{
            'subasta': self.subsession.Subasta,
            'tratamiento': self.session.config["LotSub"]
        }

class decision(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Puja']

    def vars_for_template(self):
        return {
            'subasta': self.subsession.Subasta,
            'tratamiento': self.session.config["LotSub"],
            'identificacion': self.participant.label
        }

class Ganancias(Page):
    timeout_seconds = 30
    def vars_for_template(self):
        return {
            'subasta': self.subsession.Subasta,
            'tratamiento': self.session.config["LotSub"],
            'identificacion': self.participant.label,
            'nota': "{0:.1f}".format(self.player.nota)
        }

class GananciasTotales(Page):
    form_model = 'player'
    form_fields = ['Codigo']
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]
    def vars_for_template(self): return {
        'identificacion':  self.participant.label,
        'nota': "{0:.1f}".format(self.player.nota)
    }

class espera_grupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.calcular_sorteos()
        self.subsession.seleccionar_ganador()
        jugadores=self.subsession.get_players()
        for i in jugadores:
            i.calcular_ganancia_ronda()
            i.calcular_ganancias_totales()
        self.subsession.setNotas()

class precalculos(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.set_variables_subsesion(self.round_number, self.session.config["Rounds"],
                                                self.session.config["LotSub"])
        self.subsession.inicializar_jugadores()

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
    GananciasTotales,
    gracias
]
