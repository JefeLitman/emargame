from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class presentacion(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1

class tratamientos(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"] / 2 + 1

    def vars_for_template(self):
        return {
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["SecSim"]
        }

class DecisionesAzul(Page):
    timeout_seconds = 60
    form_model = models.Player
    form_fields = ['Eleccion']

    def is_displayed(self):
        return self.player.role()=='Azul'
    def vars_for_template(self):
        return {
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["SecSim"]
        }

class DecisionesVerde(Page):
    timeout_seconds = 60
    form_model = models.Player
    form_fields = ['Eleccion']

    def is_displayed(self):
        if (self.session.config["SecSim"]):
            return self.player.role() == 'Verde' and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.role() == 'Verde' and self.round_number <= self.session.config["Rounds"] / 2
    def vars_for_template(self):
        return {
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["SecSim"]
        }

class DecisionesVerdeSEC(Page):
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
            'eleccion_otro':self.player.get_others_in_group()[0].Eleccion,
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["SecSim"]
            }


class GananciasAzul(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.player.role() == 'Azul'
    def vars_for_template(self):
        return {
            'eleccion_otro':self.player.get_others_in_group()[0].Eleccion,
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["SecSim"]
        }

class GananciasVerde(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.player.role() == 'Verde'
    def vars_for_template(self):
        return {
            'eleccion_otro':self.player.get_others_in_group()[0].Eleccion,
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["SecSim"]
        }

class GananciasTotal(Page):
    form_model = 'player'
    form_fields = ['Codigo']
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class calculo_eleccion(WaitPage):
    def after_all_players_arrive(self):
        jugador_azul = self.group.get_player_by_id(1)
        if (jugador_azul.Eleccion not in range(1,2 + 1)):
            jugador_azul.set_eleccion_azar()

class calculos(WaitPage):
    def after_all_players_arrive(self):
        jugador_verde = self.group.get_player_by_id(2)
        if (jugador_verde.Eleccion not in range(1,2 + 1)):
            jugador_verde.set_eleccion_azar()
        for p in self.group.get_players():
            p.set_pagos()
            p.set_totalpagos()

class gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    presentacion,
    tratamientos,
    esperagrupos,
    DecisionesAzul,
    DecisionesVerde,
    calculo_eleccion,
    DecisionesVerdeSEC,
    esperagrupos,
    calculos,
    GananciasAzul,
    GananciasVerde,
    GananciasTotal,
    gracias
]
