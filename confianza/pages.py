from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class welcome(Page):
    form_model=models.Player
    form_fields=['genre']

    def is_displayed(self):
        return self.round_number == 1

class tratamiento(Page):
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == Constants.num_rounds/2+1

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':Constants.num_rounds/2+1
        }

class enviosin(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number<=Constants.num_rounds/2

class enviocon(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number > Constants.num_rounds / 2

    def vars_for_template(self):
        return{
            'genrep2':self.group.get_player_by_id(2).role()
        }

class retornosin(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number<=Constants.num_rounds/2

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor
        }

    def sent_back_amount_min(self):
        return c(0)

    def sent_back_amount_max(self):
        return self.group.sent_amount*Constants.multiplication_factor

class retornocon(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number > Constants.num_rounds / 2

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor,
            'genrep1':self.group.get_player_by_id(1).role()
        }

    def sent_back_amount_min(self):
        return c(0)

    def sent_back_amount_max(self):
        return self.group.sent_amount * Constants.multiplication_factor

class gananciaindividual(Page):
    pass

class gananciatotal(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class calculos(WaitPage):

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
                if matrix_jugadores[i][j].role() == 'Inventor':
                    mujeres.append(matrix_jugadores[i][j])
                else:
                    hombres.append(matrix_jugadores[i][j])
        self.subsession.set_ganancias(mujeres,hombres)

class waitforallgroups(WaitPage):
    wait_for_all_groups = True


page_sequence = [
    welcome,
    tratamiento,
    waitforallgroups,
    enviosin,
    enviocon,
    waitforallgroups,
    retornosin,
    retornocon,
    waitforallgroups,
    calculos,
    gananciaindividual,
    gananciatotal,
]
