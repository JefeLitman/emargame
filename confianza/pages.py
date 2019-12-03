from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from random import randint

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
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"]
        }

class DecisionA_SIN(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Envia']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Participante_A == 1 and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.Participante_A == 1 and self.round_number <= self.session.config["Rounds"]/2

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"],
            'identificacion': self.participant.label
        }

    def Envia_max(self):
        return c(1000)

class DecisionA_CON(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Envia']

    def is_displayed(self):
        if (self.session.config["ConSin"]):
            return self.player.Participante_A == 1 and self.round_number <= self.session.config["Rounds"]/2
        else:
            return self.player.Participante_A == 1 and self.round_number > self.session.config["Rounds"] / 2

    def vars_for_template(self):
        return{
            'color_otro_jugador': self.player.get_others_in_group()[0].role(),
            'azul_otro_jugador':self.player.get_others_in_group()[0].Azul,
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"],
            'identificacion': self.participant.label
        }

    def Envia_max(self):
        return c(1000)

class DecisionB_SIN(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Envia']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Participante_A == 0 and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.Participante_A == 0 and self.round_number<=self.session.config["Rounds"]/2

    def vars_for_template(self):
        return {
            'recibe_multiplicado': self.player.Recibe * 3,
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"],
            'identificacion': self.participant.label
        }

    def Envia_max(self):
        return self.player.Recibe*Constants.Multiplicador

class DecisionB_CON(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Envia']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Participante_A == 0 and self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.player.Participante_A == 0 and self.round_number > self.session.config["Rounds"]/2

    def vars_for_template(self):
        return {
            'color_otro_jugador':self.player.get_others_in_group()[0].role(),
            'azul_otro_jugador': self.player.get_others_in_group()[0].Azul,
            'recibe_multiplicado':self.player.Recibe*3,
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"],
            'identificacion': self.participant.label
        }

    def Envia_max(self):
        return self.player.Recibe*Constants.Multiplicador

class Ganancias(Page):
    timeout_seconds = 30
    def vars_for_template(self):
        return{
            'azules':self.subsession.get_total_azul(),
            'verdes':self.subsession.get_total_verde(),
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"],
            'identificacion': self.participant.label,
            'gananciaAcumulada': self.player.TotalPagos,
            'nota': "{0:.1f}".format(self.player.nota)
        }

class GananciaTotal(Page):
    form_model = 'player'
    form_fields = ["Codigo"]
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]
    def vars_for_template(self): return {
        'identificacion': self.participant.label,
        'gananciaAcumulada': self.player.TotalPagos,
        'nota': "{0:.1f}".format(self.player.nota)
    }

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class precalculos(WaitPage):
    def after_all_players_arrive(self):
        # Definiendo las variables de la subsesion
        self.subsession.set_variables_subsesion(self.round_number, self.session.config["Rounds"],self.session.config["ConSin"])
        # Definiendo las variables del jugador
        for j in self.group.get_players():
            j.set_participantes(self.round_number > self.session.config["Rounds"]/2)

class calculo_recibe(WaitPage):
    def after_all_players_arrive(self):
        # Definiendo el Recibe del participante B
        for p in self.group.get_players():
            if p.Participante_A == 0:
                if(p.get_others_in_group()[0].Envia not in range(0, int(Constants.Dotacion) + 1)):
                    p.get_others_in_group()[0].Envia = randint(0,Constants.Dotacion)
                p.Recibe = p.get_others_in_group()[0].Envia

class calculo_ganancias(WaitPage):
    def after_all_players_arrive(self):
        #Definiendo el Recibe del participante A
        for p in self.group.get_players():
            if p.Participante_A == 1:
                if (p.get_others_in_group()[0].Envia not in range(0, int(p.get_others_in_group()[0].Recibe)*Constants.Multiplicador + 1)):
                    p.get_others_in_group()[0].Envia = randint(0, p.get_others_in_group()[0].Recibe*Constants.Multiplicador)
                p.Recibe = p.get_others_in_group()[0].Envia
            #Calculando las ganancias de los jugadores
            p.set_pagos()
            #Calculando las ganancias totales de los jugadores
            p.set_totalpagos()
        self.subsession.setNotas()

class gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    precalculos,
    presentacion,
    tratamientos,
    esperagrupos,
    DecisionA_SIN,
    DecisionA_CON,
    esperagrupos,
    calculo_recibe,
    DecisionB_SIN,
    DecisionB_CON,
    esperagrupos,
    calculo_ganancias,
    esperagrupos,
    Ganancias,
    GananciaTotal,
    gracias
]
