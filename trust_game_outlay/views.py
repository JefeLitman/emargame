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
        return self.player.id_in_group == 1 and self.round_number > Constants.num_rounds / 2

    def vars_for_template(self):
        p2=self.player.get_others_in_group()[0]
        if p2.get_genre() == 1:
            genero='Mujer'
        else:
            genero='Hombre'
        return{
            'genrep2':genero,
            'p2':p2.get_genre()
        }

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
        return self.player.id_in_group == 2 and self.round_number > Constants.num_rounds / 2

    def vars_for_template(self):
        p1=self.player.get_others_in_group()[1]
        if p1.get_genre() == 1:
            genero='Mujer'
        else:
            genero='Hombre'
        return {
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor,
            'genrep1':genero,
            'p1':p1.get_genre()
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
        p1.gananciajugador = p1.gananciajugador + p1.payoff
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
