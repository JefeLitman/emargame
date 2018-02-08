from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class welcome(Page):
    pass

class decision(Page):
    pass

class ganancias_sin(Page):
    pass

class ganancias_con(Page):
    pass

class ganancias_totales(Page):
    pass

class espera_grupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):

    def after_all_players_arrive(self):
        pass


page_sequence = [
    welcome,
    espera_grupos,
    decision,
    espera_grupos,
    calculos,
    ganancias_sin,
    ganancias_con,
    ganancias_totales
]
