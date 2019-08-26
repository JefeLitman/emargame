from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import randint

class introduccion(Page):

    def is_displayed(self):
        return self.round_number == 1

class consentimiento(Page):
    form_model = 'player'
    form_fields = ['consentimiento']
    def is_displayed(self):
        return self.round_number == 1

class formulario(Page):
    form_model = 'player'
    form_fields = ['nombre', 'celular', 'correo', 'genero', 'edad','semestre', 'participacion','estudiante','carrera','universidad','profesion']

    def is_displayed(self):
        return self.round_number == 1 and  self.player.in_round(1).consentimiento == True

class preguntas(Page):
    def is_displayed(self):
        return self.round_number == 1 and  self.player.in_round(1).consentimiento == True

class instruccionesAzar(Page):
    def is_displayed(self):
        return self.group.id_grupo == 1 and  self.round_number == 1 and  self.player.in_round(1).consentimiento == True

class instruccionesCompetencia(Page):
    def is_displayed(self):
        return self.group.id_grupo == 2 and  self.round_number == 1 and  self.player.in_round(1).consentimiento == True

class instruccionesVotacion(Page):
    def is_displayed(self):
        return self.group.id_grupo == 3 and  self.round_number == 1 and  self.player.in_round(1).consentimiento == True

class propuesta(Page):
    form_model = 'player'
    form_fields = ['propuesta']

    def is_displayed(self):
        return self.player.in_round(1).consentimiento == True

class propuesta_votacion(Page):
    form_model = 'player'
    form_fields = ['propuesta']

    def is_displayed(self):
        return self.group.id_grupo == 3 and self.group.set_presidente_votacion() == False and  self.player.in_round(1).consentimiento == True

class esperaJugadores(WaitPage):
    def after_all_players_arrive(self):
        self.group.inicializar_orden_llegada()
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
        return self.group.id_grupo==2 and self.player.in_round(1).consentimiento == True
    def vars_for_template(self):
        return {
            'ronda': self.round_number
        }

class termino_prueba(Page):
    timeout_seconds = 1
    def is_displayed(self):
        return self.group.id_grupo == 2 and self.player.in_round(1).consentimiento == True
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

    def vars_for_template(self):
        id_otros=[]
        propuestas = []
        for j in self.player.get_others_in_group():
            if j.propuesta != None:
                id_otros.append(j.id_in_group)
                propuestas.append(j.propuesta)
        return {
            'id_otros':id_otros,
            'propuestas':propuestas,
            'contador' : self.group.contador
        }
    def is_displayed(self):
        return self.group.id_grupo == 3 and self.group.set_presidente_votacion() == False and  self.player.in_round(1).consentimiento == True

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
        return  self.player.es_presidente == True and  self.player.in_round(1).consentimiento == True

class opinionJugadores(Page):
    form_model = 'player'
    form_fields = ['opinion']

    def is_displayed(self):
        return  self.player.es_presidente == False and  self.player.in_round(1).consentimiento == True

    def vars_for_template(self):
        jugadores = self.group.get_players()
        for jugador in jugadores:
            if(jugador.es_presidente):
                presidente = jugador
        return {'propuesta':presidente.propuesta}

class calcularganancias(WaitPage):
    def after_all_players_arrive(self):
        self.group.calcularGananciasJugadores()

class Ganancias(Page):
    def vars_for_template(self):
        longitud = 0
        for j in self.group.get_players():
            if (j.propuesta != None):
                longitud = longitud + 1
        return {'rentabilidad':(self.group.BolsaPublica * Constants.multiplicador)/longitud}
    def is_displayed(self):
        return self.player.in_round(1).consentimiento == True

class gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
    introduccion,
    consentimiento,
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

