from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class presentacion(Page):
    timeout_seconds = 30
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

class DecisionVendedor(Page):
    timeout_seconds = 60
    form_model = models.Group
    form_fields = ['Precio']

    def Precio_max(self):
        return c(2000)

    def Precio_min(self):
        return self.group.Costo

    def is_displayed(self):
        return self.player.Vendedor==True

class DecisionComprador(Page):
    timeout_seconds = 60
    form_model = models.Group
    form_fields = ['MPDA']

    def MPDA_max(self):
        return self.group.Valor

    def MPDA_min(self):
        return c(0)

    def is_displayed(self):
        return self.player.Vendedor==False

class SINGanancia(Page):
    timeout_seconds = 30
    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.round_number>self.session.config["Rounds"]/2
        else:
            return self.round_number<=self.session.config["Rounds"]/2

class CONGanancias(Page):
    timeout_seconds = 30
    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.round_number<=self.session.config["Rounds"]/2
        else:
            return self.round_number>self.session.config["Rounds"]/2

class GananciaTotal(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

class espera_grupos(WaitPage):
    wait_for_all_groups = True

class precalculos(WaitPage):

    def after_all_players_arrive(self):
        #Definiendo las variables de la subsesion
        self.subsession.set_variables_subsesion(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])
        # Definiendo las variables del grupo
        self.group.set_variables_azar()
        # Definiendo las variables del jugador
        for j in self.group.get_players():
            j.set_vendedor()

class calculos(WaitPage):

    def after_all_players_arrive(self):
        if(self.session.config["ConSin"]):
            if(self.round_number <= self.session.config["Rounds"]):
                if(self.group.Precio <= self.group.MPDA):
                    if(self.group.RRevision<=20):#Se revisa la transaccion
                        self.group.set_pagos(2)
                    else:
                        self.group.set_pagos(1)
                else:
                    self.group.set_pagos(3)
            else:
                if(self.group.Precio <= self.group.MPDA):
                    self.group.set_pagos(1)
                else:
                    self.group.set_pagos(3)
        else:
            if(self.round_number <= self.session.config["Rounds"]):
                if(self.group.Precio <= self.group.MPDA):
                    self.group.set_pagos(1)
                else:
                    self.group.set_pagos(3)
            else:
                if(self.group.Precio <= self.group.MPDA):
                    if(self.group.RRevision<=20):#Se revisa la transaccion
                        self.group.set_pagos(2)
                    else:
                        self.group.set_pagos(1)
                else:
                    self.group.set_pagos(3)
        p1 = self.group.get_player_by_id(1).set_totalpagos()
        p2 = self.group.get_player_by_id(2).set_totalpagos()

page_sequence = [
    presentacion,
    tratamientos,
    espera_grupos,
    precalculos,
    DecisionVendedor,
    DecisionComprador,
    espera_grupos,
    calculos,
    SINGanancia,
    CONGanancias,
    GananciaTotal
]
