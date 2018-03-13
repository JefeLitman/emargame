from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class bienvenida(Page):

    def is_displayed(self):
        return self.round_number == 1

class sin(Page):
        def is_displayed(self):
            return  self.round_number ==1

class con_(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds / 2

class dec_com_con(Page):
    form_model = 'group'
    form_fields = ['decision_comprador']
    def is_displayed(self):
        return self.player.role()=='Comprador' and self.round_number > Constants.num_rounds/2

class dec_com_sin(Page):
    form_model = 'group'
    form_fields = ['decision_comprador']
    def is_displayed(self):
        return self.player.role()=='Comprador' and self.round_number <= Constants.num_rounds/2

class dec_ven_con(Page):
    form_model = 'group'
    form_fields = ['calidad_real','calidad_ofrecida','precio_vendedor','decision_vendedor']
    def is_displayed(self):
        return self.player.role()=='Vendedor' and self.round_number > Constants.num_rounds/2
    def precio_vendedor_min(self):
        return Constants.costo[self.group.calidad_real-1] #Aqui hice la validacion
    def decision_vendedor_error_message(self,values): # Con esta funcion hago validaciones dinamicas de cualquier tipo para cualquier campo
        #Solo es colocar el nombre del campo y seguido viene el error message
        if (values["calidad_real"] != values["calidad_ofrecida"] and values["decision_vendedor"]):
            return 'Las calidades deben ser iguales para asegurar la calidad' #Listo

class dec_ven_sin(Page):
    form_model = 'group'
    form_fields = ['calidad_real','calidad_ofrecida','precio_vendedor']
    def is_displayed(self):
        return self.player.role()=='Vendedor' and self.round_number <= Constants.num_rounds/2
    def precio_vendedor_min(self):
        return Constants.costo[self.group.calidad_real-1] #Aqui hice la validacion

#VAmos a hacer la validacion de que sean iguales en pages, es decir, aqui mismo

class gan_individual(Page):
    pass

class gan_totales(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        p1=self.group.get_player_by_id(1)
        p2=self.group.get_player_by_id(2)
        p1.ganancias_totales=sum([p.payoff for p in self.group.get_player_by_id(1).in_all_rounds()])
        p2.ganancias_totales = sum([p.payoff for p in self.group.get_player_by_id(2).in_all_rounds()])

page_sequence = [
    bienvenida,
    sin,
    esperagrupos,
    dec_ven_sin,
    dec_ven_con,
    esperagrupos,
    dec_com_sin,
    dec_com_con,
    esperagrupos,
    calculos,
    gan_individual,
    con_,
    gan_totales
]
