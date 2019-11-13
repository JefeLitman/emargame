from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Presentacion(Page):
    #timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1


class Tratamientos(Page):
    #timeout_seconds = 30

    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"] / 2 + 1

    def vars_for_template(self):
        return {
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"]
        }

class DecisionesSIN(Page):
    #timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Voto_Azul','Voto_Rojo','Voto_Verde','VotoNo']

    def vars_for_template(self):
        return {
            'preferencia_uno': self.player.get_orden_preferencias()[0], #mas
            'preferencia_dos': self.player.get_orden_preferencias()[1],
            'preferencia_tres': self.player.get_orden_preferencias()[2], #menos
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"],
            'identificacion':  self.participant.label
        }

    def is_displayed(self):
        if (self.session.config["ConSin"]):
            return self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.round_number <= self.session.config["Rounds"] / 2


class DecisionesCON(Page):
    #timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Voto_Azul','Voto_Rojo','Voto_Verde','VotoNo']

    def vars_for_template(self):
        return {
            'mayor_preferencia_partido': self.subsession.get_distribucion_preferencias()[0][0], #mas
            '2da_preferencia_partido': self.subsession.get_distribucion_preferencias()[0][1],
            'menor_preferencia_partido': self.subsession.get_distribucion_preferencias()[0][2],#menos
            'mayor_preferencia_numero': str(self.subsession.get_distribucion_preferencias()[1][0])+"%" ,
            '2da_preferencia_numero':str(self.subsession.get_distribucion_preferencias()[1][1])+"%",
            'menor_preferencia_numero': str(self.subsession.get_distribucion_preferencias()[1][2])+"%",
            'preferencia_uno': self.player.get_orden_preferencias()[0],
            'preferencia_dos': self.player.get_orden_preferencias()[1],
            'preferencia_tres': self.player.get_orden_preferencias()[2],
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"],
            'identificacion': self.participant.label
        }

    def is_displayed(self):
        if (self.session.config["ConSin"]):
            return self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.round_number > self.session.config["Rounds"] / 2

class EsperaJugadores(WaitPage):
    wait_for_all_groups = True

class Calculos(WaitPage):
    def after_all_players_arrive(self):
        for jugador in self.subsession.get_players():
            jugador.set_votacion_aleatorio()
        self.subsession.set_ganador()
        for jugador in self.subsession.get_players():
            jugador.set_preferencia_ganador(self.subsession.Ganador)
            jugador.setPagos()
            jugador.setTotalPagos()
        self.subsession.setNotas()

class Ganancias(Page):
    #timeout_seconds=30
    def vars_for_template(self):
        return {
            'gananciaAcumulada': self.player.TotalPagos,
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"],
            'identificacion': self.participant.label
        }

class GananciasTotales(Page):
    form_model = 'player'
    form_fields = ['Codigo']
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]
    def vars_for_template(self):
        return {
            'identificacion': self.participant.label
        }

class Gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    Presentacion,
    Tratamientos,
    EsperaJugadores,
    DecisionesSIN,
    DecisionesCON,
    EsperaJugadores,
    Calculos,
    Ganancias,
    GananciasTotales,
    Gracias
]
