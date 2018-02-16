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
    num_rounds = 20
    dotacion= c(1200)


class Subsession(BaseSubsession):
    c_publica = models.CurrencyField()
    rentabilidad= models.CurrencyField()

    def calc_rent(self):
        plyers=self.get_players()
        long = len(plyers)
        return (self.c_publica*3)/long

    def calc_pub(self):
        plyers = self.get_players()
        return sum(plyers.da_c)



class Group(BaseGroup):
    def pareja(self):





class Player(BasePlayer):
    da_c=models.CurrencyField(initial=c(0),choices=currency_range(c(0),c(1000),c(1)))
    da_i = models.CurrencyField(initial=c(0), choices=currency_range(c(0), c(200), c(1)))
    punt_ind=models.CurrencyField()
    ganacias_totales=models.CurrencyField(initial=c(0)) #sum de todas las rondas

    def cal_gan_totales(self):
         self.ganacias_totales = sum([p.payoff for p in self.player.in_all_rounds()])