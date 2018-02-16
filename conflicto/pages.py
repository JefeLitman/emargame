from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class bienvenida(Page):

    def is_displayed(self):
        return self.round_number == 1

<<<<<<< HEAD
class decision_sim(Page):
    form_model = 'group'
    form_fields = ['opcion_azul','opcion_verde']
=======
class decision_sim_azul(Page):
    form_model = models.Group
    form_fields = ['opcion_azul']
>>>>>>> 62657a692fe57ed16de5f2410586b700ccc01e49

    def is_displayed(self):
        return self.player.role()=='Azul'

class decision_sim_verde(Page):
    form_model = models.Group
    form_fields = ['opcion_verde']

    def is_displayed(self):
        return self.player.role() == 'Verde' and self.round_number <= Constants.num_rounds/2

class decision_sec_verde(Page):
    form_model = 'group'
    form_fields = ['opcion_verde']

    def is_displayed(self):
        return self.player.role() == 'Verde' and self.round_number > Constants.num_rounds/2

class gan_individual(Page):
    pass

class gan_totales(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class precalculos(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_random_variables()

class calculos(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p1.ganancias_totales = sum([p.payoff for p in self.group.get_player_by_id(1).in_all_rounds()])
        p2.ganancias_totales = sum([p.payoff for p in self.group.get_player_by_id(2).in_all_rounds()])

page_sequence = [
    bienvenida,
    esperagrupos,
    precalculos,
    decision_sim_azul,
    decision_sim_verde,
    esperagrupos,
    decision_sec_verde,
    esperagrupos,
    calculos,
    gan_individual,
    gan_totales
]
