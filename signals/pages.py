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
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"]/2 +1

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"]
        }

class DecisionVendedorSin(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['Calidad','Mensaje','Precio']
    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Vendedor == True and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.Vendedor == True and self.round_number <= self.session.config["Rounds"] / 2
    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"],
            'identificacion': self.participant.label
        }

class DecisionVendedorCon(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['Calidad','Mensaje','Precio','Senal']
    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Vendedor == True and self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.player.Vendedor == True and self.round_number > self.session.config["Rounds"] / 2
    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"],
            'identificacion': self.participant.label
        }

class DecisionCompradorSin(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['Transaccion']
    def is_displayed(self):
        if (self.session.config["ConSin"]):
            return self.player.Vendedor == False and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.Vendedor == False and self.round_number <= self.session.config["Rounds"] / 2
    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"],
            'identificacion': self.participant.label
        }

class DecisionCompradorCon(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['Transaccion']
    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Vendedor == False and self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.player.Vendedor == False and self.round_number > self.session.config["Rounds"] / 2
    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"],
            'identificacion': self.participant.label,
            'nota': "{0:.1f}".format(self.player.nota)
        }

class Ganancia(Page):
    timeout_seconds = 30

    def vars_for_template(self):
        return{
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
        'nota': "{0:.1f}".format(self.player.nota)
    }

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class precalculos(WaitPage):
    def after_all_players_arrive(self):
        #Definiendo las variables de la subsesion
        self.subsession.set_variables_subsesion(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])
        # Definiendo las variables del jugador
        for j in self.group.get_players():
            j.set_vendedor()

class calculos_vendedor(WaitPage):
    def after_all_players_arrive(self):
        if (self.group.Calidad not in range(1,len(Constants.Valores) + 1)):
            self.group.set_calidad_azar()
        if (self.group.Mensaje not in range(1,len(Constants.Valores) + 1)):
            self.group.set_mensaje_azar()
        if (self.group.Precio not in range(int(Constants.Costos[0]),int(Constants.Valores[-1]) + 1)):
            self.group.set_precio_azar()
        if (self.group.Senal not in range(0,1 +1)):
            self.group.set_senal_azar(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])

class calculos(WaitPage):
    def after_all_players_arrive(self):
        if (self.group.Transaccion not in range(0,1 +1)):
            self.group.set_transaccion_azar()
        self.group.set_pagos()
        self.group.set_costo_valor()
        self.subsession.setNotas()

class gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]


page_sequence = [
    precalculos,
    presentacion,
    tratamientos,
    esperagrupos,
    DecisionVendedorSin,
    DecisionVendedorCon,
    esperagrupos,
    calculos_vendedor,
    DecisionCompradorSin,
    DecisionCompradorCon,
    esperagrupos,
    calculos,
    Ganancia,
    GananciaTotal,
    gracias
]
