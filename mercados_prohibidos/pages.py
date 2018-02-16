from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class welcome(Page):
    def is_displayed(self):
        return self.round_number == 1

class decision_vendedor(Page):
    form_model = models.Group
    form_fields = ['precio_vendedor']

    def is_displayed(self):
        return self.player.role()=='Vendedor'

class decision_comprador(Page):
    form_model = models.Group
    form_fields = ['valoracion_comprador']

    def is_displayed(self):
        return self.player.role()=='Comprador'

class ganancias_sin(Page):

    def is_displayed(self):
        return self.round_number <= Constants.num_rounds/2

class ganancias_con(Page):

    def is_displayed(self):
        return self.round_number > Constants.num_rounds/2

class ganancias_totales(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class espera_grupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):

    def after_all_players_arrive(self):
        if (self.round_number <= Constants.num_rounds and self.group.precio_vendedor <= self.group.valoracion_comprador):
            self.group.set_payoff(1)
        elif (self.round_number > Constants.num_rounds and self.group.precio_vendedor <= self.group.valoracion_comprador):
            if (self.group.revision > 20):
                self.group.set_payoff(1)
            else:
                self.group.set_payoff(2)
        else:
            self.group.set_payoff(3)
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p1.ganancias_totales = sum([p.payoff for p in self.group.get_player_by_id(1).in_all_rounds()])
        p2.ganancias_totales = sum([p.payoff for p in self.group.get_player_by_id(2).in_all_rounds()])

page_sequence = [
    welcome,
    espera_grupos,
    decision_vendedor,
    decision_comprador,
    espera_grupos,
    calculos,
    ganancias_sin,
    ganancias_con,
    ganancias_totales
]
