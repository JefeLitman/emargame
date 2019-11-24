from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint,random
from sklearn.preprocessing import MinMaxScaler

author = 'Luis Alejandro Palacio García & Bryan Snehider Díaz & Álvaro Javier Vargas Villamizar'

doc = """
Adaptando el protocolo propuesto por Goeree y Holt (1999), este juego permite analizar, entender 
y discutir la pérdida de recursos asociada a la competencia por alcanzar un premio, bajo dos 
mecanismos, subasta y lotería. La pregunta de investigación es:<br>
<br>¿Cómo afecta el mecanismo de asignación del ganador del premio la pérdida social de recursos?
<br>Se muestra como los jugadores compiten invirtiendo recursos por ganar un único premio. 
Todos los recursos invertidos en la competencia son una pérdida social, que incluso puede superar 
el valor del premio.
<br><br>Goeree, J., & Holt, C. (1999). Classroom games: Rent-seeking and the inefficiency 
of non-market allocations. Journal of Economic Perspectives, 13(3), 217–226.
"""


class Constants(BaseConstants):
    name_in_url = 'buscadores_renta'
    players_per_group = None
    num_rounds = 20
    Dotacion=c(500)

class Subsession(BaseSubsession):
    Reinicio = models.BooleanField()
    Subasta = models.BooleanField()

    def set_variables_subsesion(self, ronda, rondas_totales, consin):
        self.Reinicio = ronda > rondas_totales / 2
        if (consin):
            if (ronda <= rondas_totales / 2):
                self.Subasta = False
            else:
                self.Subasta = True
        else:
            if (ronda <= rondas_totales / 2):
                self.Subasta = True
            else:
                self.Subasta = False

    def seleccionar_ganador(self):
        jugadores = self.get_players()
        Sorteos = [jugador.Sorteo for jugador in jugadores]
        for jugador in jugadores:
            if jugador.Sorteo == max(Sorteos):
                jugador.Ganador = True
            else:
                jugador.Ganador = False

    def inicializar_jugadores(self):
        jugadores=self.get_players()
        for jugador in jugadores:
            jugador.calcular_premio()
            jugador.calcular_random()

    def calcular_sorteos(self):
        jugadores = self.get_players()
        for jugador in jugadores:
            if jugador.Puja not in range(0,int(Constants.Dotacion) + 1):
                jugador.Puja = randint(0,Constants.Dotacion)
            jugador.calcular_valor_sorteo(self.Subasta)

    def getPagosTotalesJugadores(self):
        jugadores = self.get_players()
        PagosTotalesJugadores = []
        for j in jugadores:
            PagosTotalesJugadores.append([j.TotalPagos])
        return PagosTotalesJugadores

    def getPuntajesCalificaciones(self):
        Puntajes = self.getPagosTotalesJugadores()
        scaler = MinMaxScaler(feature_range=(3.0, 5.0))
        Calificaciones = scaler.fit_transform(Puntajes)

        return Calificaciones

    def setNotas(self):
        jugadores = self.get_players()
        calificaciones = self.getPuntajesCalificaciones()
        for j in range(len(jugadores)):
            jugadores[j].Calificacion = calificaciones[j]

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Puja=models.CurrencyField(min=c(0),max=Constants.Dotacion,blank=True)
    Random = models.FloatField()
    Premio = models.CurrencyField()
    Sorteo = models.FloatField()
    Ganador=models.BooleanField()
    Pagos = models.CurrencyField()
    TotalPagos = models.CurrencyField()
    Codigo = models.StringField()
    Calificacion = models.FloatField()

    def calcular_random(self):
        self.Random = random()

    def calcular_valor_sorteo(self,Subasta):
        if(Subasta):
            self.Sorteo = float(self.Puja) + self.Random
        else:
            self.Sorteo = float(self.Puja) * self.Random

    def calcular_premio(self):
        self.Premio=randint(1000,5000)

    def calcular_ganancias_totales(self):
        self.TotalPagos=sum([p.Pagos for p in self.in_all_rounds()])

    def calcular_ganancia_ronda(self):
        if self.Ganador:
            self.Pagos=Constants.Dotacion - self.Puja + self.Premio
        else:
            self.Pagos = Constants.Dotacion - self.Puja
        self.payoff = self.Pagos