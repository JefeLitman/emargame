from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint
from sklearn.preprocessing import MinMaxScaler

author = 'Luis Alejandro Palacio García & Ferley Rincon'

doc = """
Tomando como inspiración la literatura relacionada con los castigos antisociales expuesta en Herrmann, 
Thöni, y Gächter (2008), este juego permite analizar, entender y discutir si la posibilidad de recibir 
premios o castigos afecta la contribución a un bien público. La pregunta de investigación es:<br>
<br>¿Cómo afecta la decisión de contribuir a la cuenta pública el hecho de estar expuesto a 
recibir premios o castigos?
<br>¿Los participantes están dispuestos a invertir sus puntos para incentivar a la pareja?
<br>¿Se premiará al que contribuye y se castigará al que no lo haga?
<br>Se espera que tener información sobre la contribución de la pareja cree un mecanismo presión 
social sobre la decisión de contribuir al bien público. En este sentido, no es claro si la 
contribución promedio será mayor bajo el incentivo de castigo que cuando se puede dar un premio.
<br/><br/>
Herrmann, B., Thöni, C., & Gächter, S. (2008). Antisocial punishment across societies. Science, 319(5868), 1362–1367.
"""


class Constants(BaseConstants):
    name_in_url = 'garrote_zanahoria'
    players_per_group = 2
    num_rounds = 20
    dotacion= c(1200)


class Subsession(BaseSubsession):
    ContribucionTotal = models.CurrencyField()
    Rentabilidad= models.CurrencyField()
    Reinicio=models.BooleanField()
    TMAS=models.BooleanField()

    def set_variables_subsesion(self,ronda,rondas_totales,masmenos):
        #Definiendo la variable de reinicio
        self.Reinicio = ronda > rondas_totales / 2
        # Definiendo la variable de TMAS
        if (masmenos):
            if (ronda <= rondas_totales/2):
                self.TMAS= True
            else:
                self.TMAS = False
        else:
            if (ronda <= rondas_totales/2):
                self.TMAS = False
            else:
                self.TMAS = True

    def creating_session(self):
        self.group_randomly()

    def set_rentabilidad(self):
        players=self.get_players()
        longitud_jugadores = len(players)
        self.Rentabilidad=round((self.ContribucionTotal*3)/longitud_jugadores)

    def set_contribuciontotal(self):
        players = self.get_players()
        self.ContribucionTotal=sum([p.Contribucion for p in players])

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
    def cal_incentivo_corres(self,garrote,rentabilidad):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.set_pagos(garrote,p2.Inversion,rentabilidad)
        p2.set_pagos(garrote,p1.Inversion,rentabilidad)
        p1.set_totalpagos()
        p2.set_totalpagos()

class Player(BasePlayer):
    Codigo=models.StringField()
    Pagos=models.CurrencyField()
    TotalPagos=models.CurrencyField()
    Contribucion = models.CurrencyField(blank=True,min=c(0),max=c(1000))
    Inversion = models.CurrencyField(blank=True,min=c(0),max=c(200))
    Incentivo = models.CurrencyField()
    Calificacion = models.FloatField()

    def set_pagos(self,garrote,inversion_otro,rentabilidad):
        self.Incentivo=3*inversion_otro
        if garrote == "garrote":
            self.Pagos= Constants.dotacion-(self.Inversion+self.Contribucion)+rentabilidad-self.Incentivo
        else:
            self.Pagos= Constants.dotacion-(self.Inversion+self.Contribucion)+rentabilidad+self.Incentivo
        self.payoff=self.Pagos

    def set_totalpagos(self):
         self.TotalPagos = sum([p.Pagos for p in self.in_all_rounds()])

    def set_contribucion_azar(self):
        self.Contribucion=randint(0,1000)

    def set_inversion_azar(self):
        self.Inversion=randint(0,200)
