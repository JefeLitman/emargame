from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class precalculos(WaitPage):
    def after_all_players_arrive(self):
        #Definiendo las variables de la subsesion
        self.subsession.set_variables_subsesion(self.round_number,self.session.config["Rounds"],self.session.config["MasMenos"])

class presentacion(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1

class tratamientos(Page):
    timeout_seconds=30
    def is_displayed(self):
        return self.round_number == 1 or self.round_number == self.session.config["Rounds"]/2 +1

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["MasMenos"]
        }

class contribucion(Page):
    timeout_seconds=60
    form_model = 'player'
    form_fields = ['Contribucion']

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["MasMenos"],
            'identificacion': self.participant.label
        }

class calculo_contribucion(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            if(p.Contribucion not in range(0,1000 + 1)):
                p.set_contribucion_azar()

class Incentivos(Page):
    timeout_seconds=60
    form_model = 'player'
    form_fields = ['Inversion']

    def vars_for_template(self):
        otro_jugador = self.player.get_others_in_group()[0]
        return {'contri_otro_jugador':otro_jugador.Contribucion,
                'numeroronda':self.round_number,
                'rondastotales':self.session.config["Rounds"]/2 +1,
                'tratamiento':self.session.config["MasMenos"],
                'identificacion':  self.participant.label
                }


class espera_grupos(WaitPage):
    wait_for_all_groups = True

class calculos(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            if(p.Inversion not in range(0,200 + 1)):
                p.set_inversion_azar()
        self.subsession.set_contribuciontotal()
        self.subsession.set_rentabilidad()
        if self.session.config["MasMenos"]==False:
            if self.round_number <= self.session.config["Rounds"]/2:
                self.group.cal_incentivo_corres(garrote="garrote",rentabilidad=self.subsession.Rentabilidad)
            else:
                self.group.cal_incentivo_corres(garrote="zanahoria",rentabilidad=self.subsession.Rentabilidad)
        else:
            if self.round_number <= self.session.config["Rounds"]/2:
                self.group.cal_incentivo_corres(garrote="zanahoria",rentabilidad=self.subsession.Rentabilidad)
            else:
                self.group.cal_incentivo_corres(garrote="garrote",rentabilidad=self.subsession.Rentabilidad)
        self.subsession.setNotas()

class Ganancias(Page):
    timeout_seconds=30

    def vars_for_template(self):
        return{
            'numeroronda':self.round_number,
            'rondastotales':self.session.config["Rounds"]/2 +1,
            'tratamiento':self.session.config["MasMenos"],
            'gananciaAcumulada': self.player.TotalPagos,
            'identificacion': self.participant.label,
            'nota': "{0:.1f}".format(self.player.nota)
        }

class GananciaTotal(Page):
    form_model = 'player'
    form_fields = ["Codigo"]
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]
    def vars_for_template(self): return  {
        'identificacion': self.participant.label,
        'nota': "{0:.1f}".format(self.player.nota)
    }

class gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    precalculos,
    presentacion,
    tratamientos,
    espera_grupos,
    contribucion,
    calculo_contribucion,
    espera_grupos,
    Incentivos,
    espera_grupos,
    calculos,
    Ganancias,
    GananciaTotal,
    gracias
]
