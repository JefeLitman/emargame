from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class bienvenida(Page):
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

class dec_ven_sin(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['Calidad','Mensaje','Precio']
    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Vendedor == True and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.Vendedor == True and self.round_number <= self.session.config["Rounds"] / 2

class dec_ven_con(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['Calidad','Mensaje','Precio','Senal']
    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Vendedor == True and self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.player.Vendedor == True and self.round_number > self.session.config["Rounds"] / 2

class dec_com_sin(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['Transaccion']
    def is_displayed(self):
        if (self.session.config["ConSin"]):
            return self.player.Vendedor == False and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.Vendedor == False and self.round_number <= self.session.config["Rounds"] / 2

class dec_com_con(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['Transaccion']
    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Vendedor == False and self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.player.Vendedor == False and self.round_number > self.session.config["Rounds"] / 2

class gan_individual(Page):
    timeout_seconds = 30

class gan_totales(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

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
        if (self.group.Calidad == None):
            self.group.set_calidad_azar()
        if (self.group.Mensaje == None):
            self.group.set_mensaje_azar()
        if (self.group.Precio == None):
            self.group.set_precio_azar()
        if (self.group.Senal == None):
            self.group.set_senal_azar(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])

class calculos(WaitPage):
    def after_all_players_arrive(self):
        if (self.group.Transaccion == None):
            self.group.set_transaccion_azar()
        self.group.set_pagos()
        self.group.set_costo_valor()

page_sequence = [
    precalculos,
    bienvenida,
    tratamientos,
    esperagrupos,
    dec_ven_sin,
    dec_ven_con,
    esperagrupos,
    calculos_vendedor,
    dec_com_sin,
    dec_com_con,
    esperagrupos,
    calculos,
    gan_individual,
    gan_totales
]
