from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Presentacion(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1


class tratamientos(Page):
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
            'preferencia_uno': self.player.set_orden_preferencias()[0], #mas
            'preferencia_dos': self.player.set_orden_preferencias()[1],
            'preferencia_tres': self.player.set_orden_preferencias()[2] #menos
        }

class DecisionesCON(Page):
    form_model = 'player'
    form_fields = ['Voto_Azul','Voto_Rojo','Voto_Verde','VotoNo']

    def vars_for_template(self):
        return {
            'mayor_preferencia': self.player.orden_votos ()[0], #mas
            '2da_preferencia': self.player.orden_votos()[1],
            'menor_preferencia': self.player.orden_votos()[2] #menos
        }

class Ganancias(Page):
    pass

class  GananciasTotales(Page):
    form_model = 'player'
    form_fields = ['Codigo']


page_sequence = [
    Presentacion,
    DecisionesSIN,
    DecisionesCON,
    Ganancias,
    GananciasTotales,
]
