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
        p2=self.group.in_round(1).get_player_by_id(2)
        if p2.get_genre() == 1:
            genero='Mujer'
        else:
            genero='Hombre'
        return{
            'genrep2':genero
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
        p1=self.group.in_round(1).get_player_by_id(1)
        if p1.get_genre() == 1:
            genero='Mujer'
        else:
            genero='Hombre'
        return {
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor,
            'genrep1':genero
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
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        gananciatotalp1=sum([p1.payoff for p1 in self.group.get_player_by_id(1).in_all_rounds()])
        gananciatotalp2 = sum([p2.payoff for p2 in self.group.get_player_by_id(2).in_all_rounds()])
        self.group.get_player_by_id(1).set_gananciajugador(gananciatotalp1)
        self.group.get_player_by_id(2).set_gananciajugador(gananciatotalp2)
        matrix_jugadores=self.subsession.get_group_matrix()
        mujeres=[]
        hombres=[]
        for i in range(0,len(matrix_jugadores),1):
            for j in range(0,len(matrix_jugadores[i]),1):
                if matrix_jugadores[i][j].in_round(1).get_genre() == 1:
                    mujeres.append(matrix_jugadores[i][j])
                else:
                    hombres.append(matrix_jugadores[i][j])
        self.subsession.set_ganancias(mujeres,hombres)

class waitforallgroups(WaitPage):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        gananciatotalp1 = sum([p1.payoff for p1 in self.group.get_player_by_id(1).in_all_rounds()])
        gananciatotalp2 = sum([p2.payoff for p2 in self.group.get_player_by_id(2).in_all_rounds()])
        self.group.get_player_by_id(1).set_gananciajugador(gananciatotalp1)
        self.group.get_player_by_id(2).set_gananciajugador(gananciatotalp2)

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
