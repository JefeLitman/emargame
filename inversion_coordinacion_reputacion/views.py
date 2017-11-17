from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

#Declaracion de paginas a usar

class bienvenida(Page):
    def is_displayed(self):
        return self.round_number == 1

class enviasin(Page):
    form_model = models.Player
    form_fields = ['inversion']

    def is_displayed(self):
        return self.round_number <= Constants.num_rounds/2

class enviacon(Page):
    form_model = models.Player
    form_fields = ['inversion']

    def is_displayed(self):
        return self.round_number > Constants.num_rounds/2

    def vars_for_template(self):
        if (self.round_number -1 != 0):
            otro_jugador = self.player.in_round(self.round_number-1).get_companero().calificacion_promedio
            return {
                'calificacionpromedio':otro_jugador
            }
        else:
            return {
                'calificacionpromedio':0
            }

class califica(Page):
    form_model = models.Player.get_companero()
    form_fields = ['calificacion']


class gananciastotales(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class gananciasindividuales(Page):
    pass

#Declaracion de paginas de espera

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):

    def after_all_players_arrive(self):
        #Obteniendo los jugadores por grupo
        p1=self.group.get_player_by_id(1)
        p2=self.group.get_player_by_id(2)
        #Calculando la ganancia generada por la inversion de ambos
        ganancia=self.group.calcular_gananancia(p1.inversion,p2.inversion)
        #calculando los pagos de cada jugador despues de la inversion
        p1.set_payoff(ganancia)
        p2.set_payoff(ganancia)
        #Calculo de ganancias totales por ronda
        p1ganancia=sum([j1.payoff for j1 in p1.in_all_rounds()])
        p2ganancia = sum([j2.payoff for j2 in p2.in_all_rounds()])
        p1.ganancia_total=p1ganancia
        p2.ganancia_total=p2ganancia
        #Calculando la calificacion promedio
        p1.calificacion_promedio=sum([j1.calificacion for j1 in p1.in_all_rounds()])/self.round_number
        p2.calificacion_promedio=sum([j2.calificacion for j2 in p2.in_all_rounds()])/self.round_number

page_sequence = [
    bienvenida,
    esperagrupos,
    enviasin,
    esperagrupos,
    califica,
    esperagrupos,
    calculos,
    esperagrupos,
    enviacon,
    esperagrupos,
    califica,
    esperagrupos,
    calculos,
    esperagrupos,
    gananciasindividuales,
    esperagrupos,
    gananciastotales
]
