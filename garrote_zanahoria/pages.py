from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class bienvenida(Page):
    timeout_seconds = 9999
    def is_displayed(self):
        return self.round_number == 1

class tratamientos(Page):
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"]/2 +1

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["ConSin"]
        }

class contribucion(Page):
    form_model = 'player'
    form_fields = ['da_c_pub']

class incentivo(Page):
    form_model = 'player'
    form_fields = ['da_inc']

    def vars_for_template(self):
        otro_jugador = self.player.get_others_in_group()[0]
        return {'contri_otro_jugador':otro_jugador.da_c_pub}

class espera_grupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.c_publica=self.subsession.calc_pub()
        self.subsession.rentabilidad=self.subsession.calc_rent()
        if self.session.config["ConSin"]==False:
            if self.round_number <= self.session.config["Rounds"]/2:
                self.group.cal_incentivo_corres(garrote="garrote",rentabilidad=self.subsession.rentabilidad)
            else:
                self.group.cal_incentivo_corres(garrote="zanahoria",rentabilidad=self.subsession.rentabilidad)
        else:
            if self.round_number <= self.session.config["Rounds"]/2:
                self.group.cal_incentivo_corres(garrote="zanahoria",rentabilidad=self.subsession.rentabilidad)
            else:
                self.group.cal_incentivo_corres(garrote="garrote",rentabilidad=self.subsession.rentabilidad)

class gan_individual(Page):
    pass

class gan_totales(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    bienvenida,
    tratamientos,
    espera_grupos,
    contribucion,
    espera_grupos,
    incentivo,
    espera_grupos,
    calculos,
    gan_individual,
    gan_totales
]
