from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import randint

class introduccion(Page):

    def is_displayed(self):
        return self.round_number == 1

class formulario(Page):
    form_model = 'player'
    form_fields = ['nombre', 'celular', 'correo', 'genero', 'edad','semestre', 'participacion','estudiante','carrera','universidad','consentimiento','profesion']

    def is_displayed(self):
        return self.round_number == 1

class preguntas(Page):
    def is_displayed(self):
        return self.round_number == 1

class instruccionesAzar(Page):
    def is_displayed(self):
        return self.group.id_grupo == 1

class instruccionesCompetencia(Page):
    def is_displayed(self):
        return self.group.id_grupo == 2

class instruccionesVotacion(Page):
    def is_displayed(self):
        return self.group.id_grupo == 3

class propuesta(Page):
    form_model = 'player'
    form_fields = ['propuesta']

class propuesta_votacion(Page):
    form_model = 'player'
    form_fields = ['propuesta']

    def is_displayed(self):
        return self.group.id_grupo == 3 and self.group.set_presidente_votacion() == False

class esperaJugadores(WaitPage):
    def after_all_players_arrive(self):
        self.group.inicializar_orden_llegada()
        self.group.aleatorio = randint(1,15)
        self.group.contador = 1

class eleccionAzar(WaitPage):
    def is_displayed(self):
        return self.group.id_grupo==1

    def after_all_players_arrive(self):
        self.group.set_Presidente_Azar()

class eleccionCompetencia(Page):
    form_model = 'player'
    form_fields = ['puntaje']
    def is_displayed(self):
        return self.group.id_grupo==2
    def vars_for_template(self):
        return {
            'aleatorio': self.group.aleatorio
        }

class termino_prueba(Page):
    timeout_seconds = 1
    def is_displayed(self):
        return self.group.id_grupo == 2
    def before_next_page(self):
        self.group.agregar_jugador(self.player)

class esperaCompetencia(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_presidente_competencia()
    def is_displayed(self):
        return self.group.id_grupo == 2

class eleccionVotacion(Page):
    form_model = 'player'
    form_fields = ['voto']

    ##def voto_choices(self):
        #choices=['Jugador '+str(p.id_in_group) for p in self.player.get_others_in_group()]
        #return choices
    def vars_for_template(self):
        return {
            'id_otros':[j.id_in_group for j in self.player.get_others_in_group()],
            'propuestas':[j.propuesta for j in self.player.get_others_in_group()],
            'contador' : self.group.contador
        }
    def is_displayed(self):
        return self.group.id_grupo == 3 and self.group.set_presidente_votacion() == False


class esperaTodosVoten(WaitPage):
    def after_all_players_arrive(self):
        self.group.contador += 1
    def is_displayed(self):
        return self.group.id_grupo == 3

class esperaTodosPropongan(WaitPage):
    def after_all_players_arrive(self):
        pass
    def is_displayed(self):
        return self.group.id_grupo == 3

class eleccionVotacionAzar(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_presidente_votacion_azar()

    def is_displayed(self):
        return self.group.id_grupo == 3 and self.group.set_presidente_votacion() == False

class decisionPresidente(Page):
    form_model = 'group'
    form_fields = ['BolsaPublica', 'CuentaPrivadaPresidente']

    def is_displayed(self):
        return  self.player.es_presidente == True

class opinionJugadores(Page):
    form_model = 'player'
    form_fields = ['opinion']

    def is_displayed(self):
        return  self.player.es_presidente == False 

class calcularganancias(WaitPage):
    def after_all_players_arrive(self):
        self.group.calcularGananciasJugadores()

class Ganancias(Page):
    def vars_for_template(self):
        return {'rentabilidad':(self.group.BolsaPublica * Constants.multiplicador)/len(self.group.get_players())}

class gracias(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    introduccion,
    formulario,
    instruccionesAzar,
    instruccionesCompetencia,
    instruccionesVotacion,
    preguntas,
    propuesta,
    esperaJugadores,
    eleccionAzar,
    eleccionCompetencia,
    termino_prueba,
    esperaCompetencia,
    eleccionVotacion,
    esperaTodosVoten,
    propuesta_votacion,
    esperaTodosPropongan,
    eleccionVotacion,
    esperaTodosVoten,
    propuesta_votacion,
    esperaTodosPropongan,
    eleccionVotacion,
    esperaTodosVoten,
    propuesta_votacion,
    eleccionVotacionAzar,
    decisionPresidente,
    opinionJugadores,
    esperaJugadores,
    calcularganancias,
    Ganancias,
    gracias
]

