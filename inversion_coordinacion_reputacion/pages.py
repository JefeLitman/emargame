from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

#Declaracion de paginas a usar

class bienvenida(Page):
    def is_displayed(self):
        return self.round_number == 1

class tratamiento(Page):
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["rondas"]/2 +1

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["rondas"]/2 +1,
            'tratamiento':self.session.config["tratamiento"]
        }

class enviasin(Page):
    form_model = 'player'
    form_fields = ['inversion']

    def is_displayed(self):
        if(self.session.config["tratamiento"]):
            return self.round_number > self.session.config["rondas"] / 2
        else:
            return self.round_number <= self.session.config["rondas"]/2

class enviacon(Page):
    form_model = 'player'
    form_fields = ['inversion']

    def is_displayed(self):
        if(self.session.config["tratamiento"]):
            return self.round_number <= self.session.config["rondas"] / 2
        else:
            return self.round_number > self.session.config["rondas"]/2

    def vars_for_template(self):
        if (self.round_number - 1 != 0):
            otro_jugador = self.player.get_companero().in_round(self.round_number - 1).calificacion_promedio
            return {
                'calificacionpromedio':otro_jugador
            }
        else:
            return {
                'calificacionpromedio':0
            }

class califica(Page):
    form_model =models.Player
    form_fields = ['calificacion']

    def is_displayed(self):
        if(self.session.config["tratamiento"]):
            return self.round_number <= self.session.config["rondas"] / 2
        else:
            return self.round_number > self.session.config["rondas"]/2

class gananciastotales(Page):

    def is_displayed(self):
        return self.round_number == self.session.config["rondas"]

class gananciasindividuales(Page):
    pass

#Declaracion de paginas de espera

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class calculoganancia(WaitPage):

    def after_all_players_arrive(self):
        # Obteniendo los jugadores por grupo
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        # Calculando la ganancia generada por la inversion de ambos
        ganancia = self.group.calcular_gananancia(p1.inversion, p2.inversion)
        # calculando los pagos de cada jugador despues de la inversion
        p1.set_payoff(ganancia)
        p2.set_payoff(ganancia)
        # Calculo de ganancias totales por ronda
        p1ganancia = sum([j1.payoff for j1 in p1.in_all_rounds()])
        p2ganancia = sum([j2.payoff for j2 in p2.in_all_rounds()])
        p1.ganancia_total = p1ganancia
        p2.ganancia_total = p2ganancia

class calculocalificacion(WaitPage):

    def after_all_players_arrive(self):
        #Obteniendo los jugadores por grupo
        p1=self.group.get_player_by_id(1)
        p2=self.group.get_player_by_id(2)
        #Colocando en orden las calificaciones de los jugadores
        calificacionp1=p2.calificacion
        p2.calificacion=p1.calificacion
        p1.calificacion=calificacionp1

class calculospromediocalificacion(WaitPage):
    def after_all_players_arrive(self):
        if(self.session.config["tratamiento"]):
            if (self.round_number <= self.session.config["rondas"] / 2):
                # Calculando la calificacion promedio
                p1 = self.group.get_player_by_id(1)
                p2 = self.group.get_player_by_id(2)
                p1.calificacion_promedio = sum([j.calificacion for j in p1.in_rounds(1,self.round_number)]) / (self.round_number)
                p2.calificacion_promedio = sum([j.calificacion for j in p2.in_rounds(1,self.round_number)]) / (self.round_number)
        else:
            if(self.round_number > self.session.config["rondas"]/2):
                # Calculando la calificacion promedio
                p1 = self.group.get_player_by_id(1)
                p2 = self.group.get_player_by_id(2)
                p1.calificacion_promedio = sum([j.calificacion for j in p1.in_rounds(self.session.config["rondas"] / 2 + 1, self.round_number)]) / (self.round_number - self.session.config["rondas"] / 2)
                p2.calificacion_promedio = sum([j.calificacion for j in p2.in_rounds(self.session.config["rondas"] / 2 + 1, self.round_number)]) / (self.round_number - self.session.config["rondas"] / 2)

page_sequence = [
    bienvenida,
    tratamiento,
    esperagrupos,
    enviasin,
    enviacon,
    esperagrupos,
    calculoganancia,
    gananciasindividuales,
    esperagrupos,
    califica,
    esperagrupos,
    calculocalificacion,
    esperagrupos,
    calculospromediocalificacion,
    gananciastotales
]
