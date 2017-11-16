from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

#Declaracion de paginas a usar

class bienvenida(Page):
    pass

class enviasin(Page):
    pass

class enviacon(Page):
    pass

class califica(Page):
    pass

class ganancias(Page):
    pass

#Declaracion de paginas de espera

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):

    def after_all_players_arrive(self):
        p1=self.group.get_player_by_id(1)
        p2=self.group.get_player_by_id(2)
        ganancia=self.group.calcular_gananancia(p1.inversion,p2.inversion)
        p1.set_payoff(ganancia)
        p2.set_payoff(ganancia)

page_sequence = [
    bienvenida,
    esperagrupos,
    enviasin,
    califica,
    esperagrupos,
    calculos,
    enviacon,
    califica,
    esperagrupos,
    calculos,
    ganancias
]
