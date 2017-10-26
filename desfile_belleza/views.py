from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    form_model = models.Player
    form_fields = ['elegido','nombre_elegido']

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        matrix_jugadores = self.subsession.get_group_matrix()
        self.group.set_winner(matrix_jugadores[0])


class Results(Page):
    pass


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
