from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class instrucciones(Page):
    def is_displayed(self):
        return self.round_number == 1

class resultado(Page):
    form_model = 'player'
    form_fields = ['numero_ingresado']

    def vars_for_template(self):
        return {
            "image_path": 'Lying_Game/dados/{}.png'.format(self.player.numero_real)
        }

page_sequence = [instrucciones, resultado]
