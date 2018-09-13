from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class presentacion(Page):
    timeout_seconds = 30
    form_model=models.Player
    form_fields=['genre']

    def is_displayed(self):
        return self.round_number == 1

class tratamientos(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"]/2 +1

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"]
        }

class DecisiónA_SIN(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.id_in_group == 1 and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.id_in_group == 1 and self.round_number <= self.session.config["Rounds"]/2

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"]
        }

class DecisionA_CON(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        if (self.session.config["ConSin"]):
            return self.player.id_in_group == 1 and self.round_number <= self.session.config["Rounds"]/2
        else:
            return self.player.id_in_group == 1 and self.round_number > self.session.config["Rounds"] / 2

    def vars_for_template(self):
        return{
            'genrep2':self.group.get_player_by_id(2).role(),
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"]
            }

class DecisionB_SIN(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.id_in_group == 2 and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.id_in_group == 2 and self.round_number<=self.session.config["Rounds"]/2

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor,
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"]
        }

    def sent_back_amount_min(self):
        return c(0)

    def sent_back_amount_max(self):
        return self.group.sent_amount*Constants.multiplication_factor

class DecisionB_CON(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.id_in_group == 2 and self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.player.id_in_group == 2 and self.round_number > self.session.config["Rounds"]/2

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor,
            'genrep1':self.group.get_player_by_id(1).role(),
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"]
        }

    def sent_back_amount_min(self):
        return c(0)

    def sent_back_amount_max(self):
        return self.group.sent_amount * Constants.multiplication_factor

class Ganancias(Page):
    timeout_seconds = 30
    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"]
        }

class GananciaTotal(Page):
    form_model = 'player'
    form_fields = ["Codigo"]
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

class calculos(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        gananciatotalp1=sum([p1.payoff for p1 in self.group.get_player_by_id(1).in_all_rounds()])
        gananciatotalp2 = sum([p2.payoff for p2 in self.group.get_player_by_id(2).in_all_rounds()])
        self.group.get_player_by_id(1).set_gananciajugador(gananciatotalp1)
        self.group.get_player_by_id(2).set_gananciajugador(gananciatotalp2)

class calculos_ganancias_promedios(WaitPage):

    def after_all_players_arrive(self):
        matrix_jugadores = self.subsession.get_group_matrix()
        mujeres = []
        hombres = []
        for i in range(0,len(matrix_jugadores),1):
            for j in range(0,len(matrix_jugadores[i]),1):
                if matrix_jugadores[i][j].role() == 'Inventor':
                    mujeres.append(matrix_jugadores[i][j])
                else:
                    hombres.append(matrix_jugadores[i][j])
        self.subsession.set_ganancias(mujeres,hombres)

class waitforallgroups(WaitPage):
    wait_for_all_groups = True

class gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    presentacion,
    tratamientos,
    waitforallgroups,
    DecisiónA_SIN,
    DecisionA_CON,
    waitforallgroups,
    DecisionB_SIN,
    DecisionB_CON,
    waitforallgroups,
    calculos,
    waitforallgroups,
    calculos_ganancias_promedios,
    Ganancias,
    GananciaTotal,
    gracias
]
