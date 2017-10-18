from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class welcome(Page):
    form_model=models.Player
    form_fields=['genre']
    def is_displayed(self):
        return self.round_number == 1


page_sequence = [
    welcome
]
