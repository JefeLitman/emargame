from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Presentacion(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1


class Tratamientos(Page):
    timeout_seconds = 30

    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"] / 2 + 1

    def vars_for_template(self):
        return {
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["MasMenos"]
        }


class DecisionesSIN(Page):
    form_model = 'player'
    form_fields = ['Voto_Azul','Voto_Rojo','Voto_Verde','VotoNo']

    def vars_for_template(self):
        return {
            'preferencia_uno': self.player.get_orden_preferencias()[0], #mas
            'preferencia_dos': self.player.get_orden_preferencias()[1],
            'preferencia_tres': self.player.get_orden_preferencias()[2] #menos
        }


class DecisionesCON(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Voto_Azul','Voto_Rojo','Voto_Verde','VotoNo']

    def vars_for_template(self):
        return {
            'mayor_preferencia_partido': self.subsession.set_n_jugadores[0][0], #mas
            '2da_preferencia_partido': self.subsession.set_n_jugadores[0][1],
            'menor_preferencia_partido': self.subsession.set_n_jugadores[0][2],#menos
            'mayor_preferencia_numero': self.subsession.set_n_jugadores[1][0],
            '2da_preferencia_numero':self.subsession.set_n_jugadores[1][1],
            'menor_preferencia_numero': self.subsession.set_n_jugadores[1][2],
            'preferencia_uno': self.player.get_orden_preferencias()[0],
            'preferencia_dos': self.player.get_orden_preferencias()[1],
            'preferencia_tres': self.player.get_orden_preferencias()[2]
        }


class Ganancias(Page):
    timeout_seconds=30


class  GananciasTotales(Page):
    timeout_seconds = 30
    form_model = 'player'
    form_fields = ['Codigo']


class Gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    Presentacion,
    Tratamientos,
    DecisionesSIN,
    DecisionesCON,
    Ganancias,
    GananciasTotales,
    Gracias
]
