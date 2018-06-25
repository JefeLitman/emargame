from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from math import ceil

class bienvenido(Page):
    def is_displayed(self):
        return self.round_number == 1

class esperaGrupos(WaitPage):
    wait_for_all_groups = True

class calculo_NT(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_niveles_tecnologia()

class oferta_contratistas(Page):
    form_model = 'player'
    form_fields = ['cuenta_publica','cuenta_privada','soborno']
    def is_displayed(self):
        return self.player.role()=="Contratista"

class decision_burocrata(Page):
    form_model = 'group'
    form_fields = ['aceptaC1','aceptaC2','aceptaC3']
    def is_displayed(self):
        return self.player.role()=="Burocrata"
    def vars_for_template(self):
        return {
            'ntc1':self.group.get_player_by_id(2).nivel_tecnologia,
            'ntc2':self.group.get_player_by_id(3).nivel_tecnologia,
            'ntc3':self.group.get_player_by_id(4).nivel_tecnologia,
            'sobornoc1': self.group.get_player_by_id(2).soborno,
            'sobornoc2': self.group.get_player_by_id(3).soborno,
            'sobornoc3': self.group.get_player_by_id(4).soborno,
            'cpc1': self.group.get_player_by_id(2).cuenta_privada,
            'cpc2': self.group.get_player_by_id(3).cuenta_privada,
            'cpc3': self.group.get_player_by_id(4).cuenta_privada,
            'tratamiento':self.session.config["tratamiento"]
        }

class definir_ganador(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_aceptaciones()
        nivelxcp=self.group.get_nivelxcp()
        jugadores=self.group.get_players()
        for i in jugadores:
            i.set_payoff(nivelxcp)

class gan_periodo(Page):
    def vars_for_template(self):
        return {'contratista':self.player.role()!='Burocrata'}

class gan_totales(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["rondas"]
    def vars_for_template(self):
        return {
            'ronda':self.player.set_ganancias_totales(self.session.config["rondas"])
        }

page_sequence = [
    bienvenido,
    esperaGrupos,
    calculo_NT,
    oferta_contratistas,
    esperaGrupos,
    decision_burocrata,
    esperaGrupos,
    definir_ganador,
    gan_periodo,
    gan_totales
]
