from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class bienvenida(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1

class tratamiento(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"] / 2 + 1

    def vars_for_template(self):
        return {
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["SecSim"]
        }

class decision_sim_azul(Page):
    timeout_seconds = 60
    form_model = models.Player
    form_fields = ['Eleccion']

    def is_displayed(self):
        return self.player.role()=='Azul'

class decision_sim_verde(Page):
    timeout_seconds = 60
    form_model = models.Player
    form_fields = ['Eleccion']

    def is_displayed(self):
        if (self.session.config["SecSim"]):
            return self.player.role() == 'Verde' and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.role() == 'Verde' and self.round_number <= self.session.config["Rounds"] / 2

class decision_sec_verde(Page):
    timeout_seconds = 60
    form_model = models.Player
    form_fields = ['Eleccion']

    def is_displayed(self):
        if (self.session.config["SecSim"]):
            return self.player.role() == 'Verde' and self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.player.role() == 'Verde' and self.round_number > self.session.config["Rounds"] / 2

    def vars_for_template(self):
        return {
            'eleccion_otro':self.player.get_others_in_group()[0].Eleccion
        }

class gan_individual(Page):
    timeout_seconds = 30
    def vars_for_template(self):
        return {
            'eleccion_otro':self.player.get_others_in_group()[0].Eleccion
        }

class gan_totales(Page):
    form_model = 'player'
    form_fields = ['Codigo']
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class calculo_eleccion(WaitPage):
    def after_all_players_arrive(self):
        jugador_azul = self.group.get_player_by_id(1)
        if (jugador_azul.Eleccion == None):
            jugador_azul.set_eleccion_azar()

class calculos(WaitPage):
    def after_all_players_arrive(self):
        jugador_verde = self.group.get_player_by_id(2)
        if (jugador_verde.Eleccion == None):
            jugador_verde.set_eleccion_azar()
        for p in self.group.get_players():
            p.set_pagos()
            p.set_totalpagos()

page_sequence = [
    bienvenida,
    tratamiento,
    esperagrupos,
    decision_sim_azul,
    decision_sim_verde,
    calculo_eleccion,
    decision_sec_verde,
    esperagrupos,
    calculos,
    gan_individual,
    gan_totales
]
