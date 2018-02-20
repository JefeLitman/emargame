from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name'

doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'trust_game_outlay'
    players_per_group = 2
    num_rounds=10

    endowment = c(1000)
    multiplication_factor = 3


class Subsession(BaseSubsession):
    gananciamujeres=models.CurrencyField(initial=c(0))
    gananciahombres=models.CurrencyField(initial=c(0))

    def set_ganancias(self,mujeres,hombres):
        if len(mujeres) != 0:
            self.gananciamujeres = sum([p.payoff for p in mujeres])/len(mujeres)
        if len(hombres) != 0:
            self.gananciahombres = sum([p.payoff for p in hombres])/len(hombres)

    def creating_session(self):
        self.group_randomly()

class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        choices=currency_range(0,Constants.endowment,c(1)),
        initial=c(0)
    )
    sent_back_amount = models.CurrencyField(
        initial=c(0)
    )

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount

class Player(BasePlayer):
    genre=models.PositiveIntegerField(
        choices=[
            [1,'Mujer'],
            [2, 'Hombre'],
        ],
        initial=0
    )
    gananciajugador=models.CurrencyField(initial=c(0))

    def get_genre(self):
        return self.genre

    def set_gananciajugador(self,valor):
        self.gananciajugador=valor
