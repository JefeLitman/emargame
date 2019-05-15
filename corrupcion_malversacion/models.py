from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from itertools import cycle
from random import choice

author = 'Santiago Sequeda & Mayra Riascos & Edgar Rangel'

doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'malversacion'
    players_per_group = 5
    num_rounds = 10
    dotacion = c(3000)
    multiplicador = 2

class Subsession(BaseSubsession):
    def creating_session(self):
        tipos_grupo = cycle([1,2,3])
        for grupo in self.get_groups():
            grupo.id_grupo = next(tipos_grupo)

class Group(BaseGroup):
    id_grupo = models.IntegerField(doc="""Identificador del tipo de grupo de los integrantes.
    1 - Presidente al azar
    2 - Presidente por competencia
    3 - Presidente por votacion""")
    orden_llegada = models.StringField(doc="""Sera un array de letras que contendra el orden de 
    llegada de los jugadores en las diferentes rondas:
    Ej: 'id_jugador_xid_jugador_y' o '231...' """)
    BolsaPublica = models.CurrencyField(min=0,max=Constants.dotacion)
    CuentaPrivadaPresidente = models.CurrencyField(min=0,max=Constants.dotacion)
    contador = models.IntegerField()

    def inicializar_orden_llegada(self):
        self.orden_llegada = ""

    def contador_jugadores(self):
        contador = 5
        for id in self.orden_llegada:
            if int(id) in [1,2,3,4,5]:
                contador = contador - 1
        return contador

    def set_presidente(self,presidente):
        presidente.es_presidente = True
        for otros in presidente.get_others_in_group():
            otros.es_presidente = False

    def set_Presidente_Azar(self):
        presidente = choice(self.get_players())
        self.set_presidente(presidente)

    def set_presidente_competencia(self):
        puntajes = [j.puntaje for j in self.get_players()]
        for jugador in self.get_players():
            if (jugador.puntaje == max(puntajes)):
                presidente = jugador
        self.set_presidente(presidente)

    def agregar_jugador(self, jugador):
        extra = self.contador_jugadores()
        jugador.puntaje = jugador.puntaje + extra
        self.orden_llegada = self.orden_llegada + str(jugador.id_in_group)

    def set_presidente_votacion(self):
        jugadores=self.get_players()
        votos = [p.voto for p in jugadores]
        contador = 0
        for i in jugadores:
            if votos.count( 'Jugador ' + str( i.id_in_group)) >= int(len(jugadores)/2) +1 :
                presidente = i
                break
            else:
                contador = contador + 1
        if contador == len(jugadores):
            return False
        else:
            self.set_presidente(presidente)
            return True

    def set_presidente_votacion_azar(self):
        jugadores = self.get_players()
        votos = [p.voto for p in jugadores]
        numero_votos = [votos.count('Jugador ' + str(j.id_in_group)) for j in jugadores]
        posibles_presidentes =[]
        for i,cantidad in enumerate(numero_votos):
            if cantidad == max(numero_votos):
                posibles_presidentes.append(i+1)
        id_presidente = choice(posibles_presidentes)
        presidente = self.get_player_by_id(id_presidente)
        self.set_presidente(presidente)

    def calcularGananciasJugadores(self):
        rentabilidad = (self.BolsaPublica * Constants.multiplicador)/len(self.get_players())
        for j in self.get_players():
            if j.es_presidente == True:
                j.cuenta = rentabilidad + self.CuentaPrivadaPresidente
            else:
                j.cuenta = rentabilidad
            j.payoff = j.cuenta

class Player(BasePlayer):
    propuesta = models.LongStringField(max_length=140)
    cuenta = models.CurrencyField()
    es_presidente = models.BooleanField()
    puntaje = models.IntegerField()
    voto = models.StringField()
    opinion = models.BooleanField(choices=[[True, 'Si' ], [False, 'No']])
    nombre= models.StringField()
    celular= models.StringField()
    correo= models.StringField()
    genero = models.StringField(choices=['Femenino','Masculino'])
    edad = models.IntegerField()
    semestre = models.IntegerField()
    participacion = models.BooleanField(choices=[[True, 'Si' ], [False, 'No']])
    estudiante = models.BooleanField(choices=[[True, 'Si' ], [False, 'No']])
    carrera= models.StringField(blank=True)
    universidad= models.StringField(blank=True)
    consentimiento = models.BooleanField(choices=[[True, 'Si autorizo'], [False, 'No autorizo']])
    profesion = models.StringField(blank=True)
