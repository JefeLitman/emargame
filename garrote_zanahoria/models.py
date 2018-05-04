from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'garrote_zanahoria'
    players_per_group = 2
    num_rounds = 30
    dotacion= c(1200)


class Subsession(BaseSubsession):
    c_publica = models.CurrencyField(initial=c(0))
    rentabilidad= models.CurrencyField(initial=c(0))

    def creating_session(self):
        self.group_randomly()

    def calc_rent(self):
        players=self.get_players()
        long = len(players)
        return round((self.c_publica*3)/long)

    def calc_pub(self):
        players = self.get_players()
        return sum([p.da_c_pub for p in players])


class Group(BaseGroup):
    def cal_incentivo_corres(self,garrote,rentabilidad):
        p1=self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.cal_c_privada(garrote,p2.da_inc,rentabilidad)
        p2.cal_c_privada(garrote,p1.da_inc,rentabilidad)
        p1.cal_gan_totales()
        p2.cal_gan_totales()
    #def cal_cont_grupo_cp(self):
     #   p1.get_da_inc()
    #  p2.get_da_inc()


class Player(BasePlayer):
    c_privada=models.CurrencyField(initial=c(0))
    da_c_pub = models.CurrencyField(initial=c(0),min=c(0),max=c(1000))
    da_inc = models.CurrencyField(initial=c(0),min=c(0),max=c(200))
    ganacias_totales=models.CurrencyField(initial=c(0)) #sum de todas las rondas
    #gan_c_privada=models.CurrencyField(initial=c(0))

    def cal_gan_totales(self):
         self.ganacias_totales = sum([p.c_privada for p in self.in_all_rounds()])

    def cal_c_privada(self,garrote,da_inc_otro,rentabilidad):
        if garrote == "garrote":
            self.c_privada= Constants.dotacion-(self.da_inc+self.da_c_pub)+rentabilidad-3*da_inc_otro
        else:
            self.c_privada = Constants.dotacion - (self.da_inc + self.da_c_pub) + rentabilidad+3*da_inc_otro

    #def cal_gan_c_privada(self,garrote,da_inc_otro,rentabilidad):
     #   if garrote == "garrote":
      #      self.gan_c_privada= rentabilidad-3*da_inc_otro
       # else:
        #    self.gan_c__privada= rentabilidad+3*da_inc_otro

    #def get_da_inc(self):
     #   da_inc_g=self.da_inc

