from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint,random

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

    def seleccionar_ganador_subasta(self):
        jugadores=self.get_players()
        inversion_jugadores=[]
        for i in range(len(jugadores)):
            inversion_jugadores.append(jugadores[i].da_invertir+random())
        for i in range(len(inversion_jugadores)):
            if inversion_jugadores[i] == max(inversion_jugadores):
                jugadores[i].gano=True

    def seleccionar_ganador_loteria(self):
        jugadores=self.get_players()
        inversionistas=[]
        for i in range(len(jugadores)):
            if jugadores[i].da_invertir != c(0):
                inversionistas.append(jugadores[i])
        inversionistas[randint(0,len(inversionistas))].gano=True

    def calcular_valores_productos(self):
        jugadores=self.get_players()
        for i in jugadores:
            i.calcular_valor_producto()

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Puja=models.CurrencyField(min=c(0),max=Constants.Dotacion)
    Random = models.IntegerField()
    V = models.CurrencyField()
    Sorteo = models.IntegerField()
    MaxSorteo = models.IntegerField()
    Ganador=models.BooleanField()
    Pagos = models.CurrencyField()
    TotalPagos = models.CurrencyField()
    Codigo = models.StringField()

    def calcular_valor_sorteo(self,):
        pass

    def calcular_valor_producto(self):
        self.V=randint(1000,5000)

    def calcular_ganancias_totales(self):
        self.TotalPagos=sum([p.Pagos for p in self.in_all_rounds()])

    def calcular_ganancia_ronda(self):
        if self.Ganador:
            self.Pagos=Constants.Dotacion - self.Puja + self.V
        else:
            self.Pagos = Constants.Dotacion - self.Puja
        self.payoff = self.Pagos