from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class bienvenida(Page):
    pass

class dec_com_con(Page):
    pass

class dec_com_sin(Page):
    pass

class dec_ven_con(Page):
    pass

class dec_ven_sin(Page):
    pass

class etapas(Page):
    pass

class gan_individual(Page):
    pass

class gan_totales(Page):
    pass

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):
    def after_all_players_arrive(self):
        pass

page_sequence = [
    bienvenida,
    etapas,
    esperagrupos
]
