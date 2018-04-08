from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    form_model = 'player'
    form_fields = ['elegido','nombre_elegido']

    def is_displayed(self):
        return self.round_number <= self.session.config["rondas"]

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        matrix_jugadores = self.subsession.get_group_matrix()
        self.group.set_winner(matrix_jugadores[0])


class Results(Page):
    def vars_for_template(self):
        return {
            'rondas':self.session.config["rondas"],
            'ronda':self.round_number
        }

    def is_displayed(self):
        return self.round_number <= self.session.config["rondas"]


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
