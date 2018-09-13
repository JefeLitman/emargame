from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

<<<<<<< HEAD
class welcome(Page):
    timeout_seconds = 30
=======
class presentacion(Page):
    timeout_seconds = 30
    form_model=models.Player
    form_fields=['genre']
>>>>>>> 2295efcd6f73dd5f92585aaa6fd97f724d1ac2a3

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

<<<<<<< HEAD
class enviosin(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Envia']
=======
class DecisiónA_SIN(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['sent_amount']
>>>>>>> 2295efcd6f73dd5f92585aaa6fd97f724d1ac2a3

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Participante_A == 1 and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.Participante_A == 1 and self.round_number <= self.session.config["Rounds"]/2

<<<<<<< HEAD
class enviocon(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Envia']
=======
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
>>>>>>> 2295efcd6f73dd5f92585aaa6fd97f724d1ac2a3

    def is_displayed(self):
        if (self.session.config["ConSin"]):
            return self.player.Participante_A == 1 and self.round_number <= self.session.config["Rounds"]/2
        else:
            return self.player.Participante_A == 1 and self.round_number > self.session.config["Rounds"] / 2

    def vars_for_template(self):
        return{
<<<<<<< HEAD
            'color_otro_jugador':self.player.get_others_in_group()[0].role()
        }

class retornosin(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Envia']
=======
            'genrep2':self.group.get_player_by_id(2).role(),
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"]
            }

class DecisionB_SIN(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['sent_back_amount']
>>>>>>> 2295efcd6f73dd5f92585aaa6fd97f724d1ac2a3

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Participante_A == 0 and self.round_number > self.session.config["Rounds"] / 2
        else:
            return self.player.Participante_A == 0 and self.round_number<=self.session.config["Rounds"]/2

<<<<<<< HEAD
    def Envia_min(self):
=======
    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor,
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"]
        }

    def sent_back_amount_min(self):
>>>>>>> 2295efcd6f73dd5f92585aaa6fd97f724d1ac2a3
        return c(0)

    def Envia_max(self):
        return self.player.Recibe*Constants.Multiplicador

<<<<<<< HEAD
class retornocon(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['Envia']
=======
class DecisionB_CON(Page):
    timeout_seconds = 60
    form_model = 'group'
    form_fields = ['sent_back_amount']
>>>>>>> 2295efcd6f73dd5f92585aaa6fd97f724d1ac2a3

    def is_displayed(self):
        if(self.session.config["ConSin"]):
            return self.player.Participante_A == 0 and self.round_number <= self.session.config["Rounds"] / 2
        else:
            return self.player.Participante_A == 0 and self.round_number > self.session.config["Rounds"]/2

    def vars_for_template(self):
        return {
<<<<<<< HEAD
            'color_otro_jugador':self.player.get_others_in_group()[0].role()
=======
            'tripled_amount': self.group.sent_amount*Constants.multiplication_factor,
            'genrep1':self.group.get_player_by_id(1).role(),
            'numeroronda': self.round_number,
            'rondastotales': self.session.config["Rounds"] / 2 + 1,
            'tratamiento': self.session.config["ConSin"]
>>>>>>> 2295efcd6f73dd5f92585aaa6fd97f724d1ac2a3
        }

    def Envia_min(self):
        return c(0)

    def Envia_max(self):
        return self.player.Recibe*Constants.Multiplicador

<<<<<<< HEAD
class gananciaindividual(Page):
    timeout_seconds = 30

class gananciatotal(Page):
    timeout_seconds = 30
=======
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
>>>>>>> 2295efcd6f73dd5f92585aaa6fd97f724d1ac2a3
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

class precalculos(WaitPage):

    def after_all_players_arrive(self):
        #Definiendo las variables de la subsesion
        self.subsession.set_variables_subsesion(self.round_number,self.session.config["Rounds"],self.session.config["ConSin"])

class esperagrupos(WaitPage):
    wait_for_all_groups = True

class calculo_recibe(WaitPage):
    def after_all_players_arrive(self):
        # Definiendo el Recibe del participante B
        for p in self.group.get_players():
            if p.Participante_A == 0:
                p.Recibe = p.get_others_in_group()[0].Envia

class calculo_ganancias(WaitPage):
    def after_all_players_arrive(self):
        #Definiendo el Recibe del participante A
        for p in self.group.get_players():
            if p.Participante_A == 1:
                p.Recibe = p.get_others_in_group()[0].Envia
                p.set_pagos()
                p.get_others_in_group()[0].set_pagos()

class calculos_ganancias_promedios(WaitPage):
    def after_all_players_arrive(self):
        matrix_jugadores = self.subsession.get_group_matrix()
        azules = []
        verdes = []
        for i in range(0,len(matrix_jugadores),1):
            for j in range(0,len(matrix_jugadores[i]),1):
                if matrix_jugadores[i][j].role() == 'Azul':
                    azules.append(matrix_jugadores[i][j])
                else:
                    verdes.append(matrix_ju}gadores[i][j])
        self.subsession.set_ganancias(mujeres,hombres)

<<<<<<< HEAD
page_sequence = [
    precalculos,
    welcome,
    tratamientos,
    esperagrupos,
    enviosin,
    enviocon,
    esperagrupos,
    calculo_recibe,
    retornosin,
    retornocon,
    esperagrupos,
    calculo_ganancias,
=======
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
>>>>>>> 2295efcd6f73dd5f92585aaa6fd97f724d1ac2a3
    calculos_ganancias_promedios,
    Ganancias,
    GananciaTotal,
    gracias
]
