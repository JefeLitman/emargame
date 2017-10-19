from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class welcome(Page):
    form_model=models.Player
    form_fields=['genre']

    def is_displayed(self):
        return self.round_number == 1

class enviosin(Page):
    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number<=Constants.num_rounds/2

class enviocon(Page):
    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number >= Constants.num_rounds / 2

class retornosin(Page):
    form_model = models.Group
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number<=Constants.num_rounds/2

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor
        }

    def sent_back_amount_choices(self):
        return currency_range(
            c(0),
            self.group.sent_amount * Constants.multiplication_factor,
            c(1)
        )

class retornocon(Page):
    form_model = models.Group
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number >= Constants.num_rounds / 2

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor
        }

    def sent_back_amount_choices(self):
        return currency_range(
            c(0),
            self.group.sent_amount * Constants.multiplication_factor,
            c(1)
        )

class gananciaindividual(Page):
    pass

class gananciatotal(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class waitforP1(WaitPage):
    pass

class waitforP2(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        p1=self.group.get_player_by_id(1)
        p2=self.group.get_player_by_id(2)
        p1.gananciajugador=p1.gananciajugador+p1.payoff
        p2.gananciajugador = p2.gananciajugador + p2.payoff

class waitforallgroups(WaitPage):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p1.gananciajugador = p1.gananciajugador + p1.payoff
        p2.gananciajugador = p2.gananciajugador + p2.payoff

page_sequence = [
    welcome,
    enviosin,
    enviocon,
    waitforP1,
    retornosin,
    retornocon,
    waitforP2,
    gananciaindividual,
    waitforallgroups,
    gananciatotal,
]
