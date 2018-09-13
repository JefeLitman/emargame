from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

#Declaracion de paginas a usar

class presentacion(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1

class tratamiento(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"]/2 +1

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"]
        }

class DecisionesSIN(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Inversion']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.round_number <= self.session.config["Rounds"]/2
    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"]
        }

class DecisionesCON(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Inversion']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.round_number > self.session.config["Rounds"]/2

    def vars_for_template(self):
        if (self.round_number - 1 != 0):
            otro_jugador = self.player.get_others_in_group()[0].in_round(self.round_number - 1).Reputacion
            return {
                'Reputacion':otro_jugador,
                'numeroronda': self.round_number,
                'rondastotales': self.session.config["Rounds"] / 2 + 1,
                'tratamiento': self.session.config["ConSin"]
            }
        else:
            return {
                'Reputacion':5,
                'numeroronda':self.round_number,
                'rondastotales':self.session.config["Rounds"]/2 +1,
                'tratamiento':self.session.config["ConSin"]
            }

class GananciasCON(Page):
    timeout_seconds = 60
    form_model =models.Player
    form_fields = ['Calificacion']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.round_number > self.session.config["Rounds"]/2
    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"],
            'otro':self.player.get_others_in_group()[0]
        }

class GananciasSIN(Page):
    timeout_seconds = 60
    form_model =models.Player
    form_fields = ['Calificacion']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.round_number <= self.session.config["Rounds"]/2
    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"],
            'otro': self.player.get_others_in_group()[0]
        }

class GananciasTotal(Page):
    form_model = 'player'
    form_fields = ["Codigo"]
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

#Declaracion de paginas de espera

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class precalculos(WaitPage):

    def after_all_players_arrive(self):
        #Definiendo las variables de la subsesion
        self.subsession.set_variables_subsesion(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])

class calculoganancia(WaitPage):

    def after_all_players_arrive(self):
        # Obteniendo los jugadores por grupo
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        #Definiendo variables azar si no las lleno
        if (p1.Inversion == None):
            p1.set_inversion_azar()
        if (p2.Inversion == None):
            p2.set_inversion_azar()
        # Calculando la ganancia generada por la inversion de ambos
        ganancia = self.group.calcular_gananancia(p1.Inversion, p2.Inversion)
        # calculando los pagos de cada jugador despues de la inversion
        p1.set_pago(ganancia)
        p2.set_pago(ganancia)
        # Calculo de ganancias totales por ronda
        p1.set_totalpagos()
        p2.set_totalpagos()

class calculocalificacion(WaitPage):

    def after_all_players_arrive(self):
        #Obteniendo los jugadores por grupo
        p1=self.group.get_player_by_id(1)
        p2=self.group.get_player_by_id(2)
        # Definiendo variables azar si no las lleno
        if (p1.Calificacion == None):
            p1.set_calificacion_azar(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])
        if (p2.Calificacion == None):
            p2.set_calificacion_azar(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])
        #Colocando en orden las calificaciones de los jugadores
        calificacionp1=p2.Calificacion
        p2.Calificacion=p1.Calificacion
        p1.Calificacion=calificacionp1

class calculospromediocalificacion(WaitPage):
    def after_all_players_arrive(self):
        self.group.get_player_by_id(1).set_reputacion(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])
        self.group.get_player_by_id(2).set_reputacion(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])

class gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    precalculos,
    presentacion,
    tratamiento,
    esperagrupos,
    DecisionesCON,
    DecisionesSIN,
    esperagrupos,
    calculoganancia,
    GananciasSIN,
    GananciasCON,
    esperagrupos,
    calculocalificacion,
    calculospromediocalificacion,
    GananciasTotal,
    gracias
]
