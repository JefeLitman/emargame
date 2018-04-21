from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class bienvenida(Page):
    def is_displayed(self):
        return self.round_number == 1

class tratamientos(Page):
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["rondas"]/2 +1

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["rondas"]/2 +1,
            'tratamiento':self.session.config["tratamiento"]
        }

class subasta(Page):
    form_model = 'player'
    form_fields = ['da_invertir']

    def is_displayed(self):
        if(self.session.config["tratamiento"]):
            return self.round_number > self.session.config["rondas"]/2
        else:
            return self.round_number <= self.session.config["rondas"]/2

class loteria(Page):
    form_model = 'player'
    form_fields = ['da_invertir']

    def is_displayed(self):
        if (self.session.config["tratamiento"]):
            return self.round_number <= self.session.config["rondas"] / 2
        else:
            return self.round_number > self.session.config["rondas"] / 2

class ganancias_individuales(Page):
    pass

class ganancias_totales(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["rondas"]

class espera_grupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):
    def after_all_players_arrive(self):
        if (self.session.config["tratamiento"]):
            if(self.round_number<= self.session.config["rondas"]):
                self.subsession.seleccionar_ganador_loteria()
            else:
                self.subsession.seleccionar_ganador_subasta()
        else:
            if (self.round_number <= self.session.config["rondas"]):
                self.subsession.seleccionar_ganador_subasta()
            else:
                self.subsession.seleccionar_ganador_loteria()
        jugadores=self.subsession.get_players()
        for i in jugadores:
            i.calcular_ganancia_ronda()
            i.calcular_ganancias_totales()

class precalculos(WaitPage):
    def after_all_players_arrive(self):
        self.subsession.calcular_valores_productos()

page_sequence = [
    precalculos,
    bienvenida,
    tratamientos,
    espera_grupos
    subasta,
    loteria,
    espera_grupos,
    calculos,
    ganancias_individuales,
    ganancias_totales
]
