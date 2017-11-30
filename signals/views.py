from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class bienvenida(Page):

    def is_displayed(self):
        return self.round_number == 1

class dec_com_con(Page):
    form_model = models.Group
    form_fields = ['decision_comprador']
    def is_displayed(self):
        return self.player.role()=='Comprador' and self.round_number > Constants.num_rounds/2

class dec_com_sin(Page):
    form_model = models.Group
    form_fields = ['decision_comprador']
    def is_displayed(self):
        return self.player.role()=='Comprador' and self.round_number <= Constants.num_rounds/2

class dec_ven_con(Page):
    form_model = models.Group
    form_fields = ['calidad_real','calidad_ofrecida','precio_vendedor','decision_vendedor']
    def is_displayed(self):
        return self.player.role()=='Vendedor' and self.round_number > Constants.num_rounds/2

class dec_ven_sin(Page):
    form_model = models.Group
    form_fields = ['calidad_real','calidad_ofrecida','precio_vendedor']
    def is_displayed(self):
        return self.player.role()=='Vendedor' and self.round_number <= Constants.num_rounds/2

class etapas(Page):
    def is_displayed(self):
        return self.round_number == 1

class gan_individual(Page):
    pass

class gan_totales(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        p1=self.group.get_player_by_id(1)
        p2=self.group.get_player_by_id(2)
        p1.ganancias_totales=sum([p.payoff for p in self.group.get_player_by_id(1).in_all_rounds()])
        p2.ganancias_totales = sum([p.payoff for p in self.group.get_player_by_id(2).in_all_rounds()])

page_sequence = [
    bienvenida,
    etapas,
    esperagrupos,
    dec_ven_sin,
    dec_ven_con,
    esperagrupos,
    dec_com_sin,
    dec_com_con,
    esperagrupos,
    calculos,
    gan_individual,
    gan_totales
]
