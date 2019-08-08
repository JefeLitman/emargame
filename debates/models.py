from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'debates'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    promI1AF = models.FloatField()
    promI2AF = models.FloatField()
    promI3AF = models.FloatField()
    promI4AF = models.FloatField()
    promI5AF = models.FloatField()
    promI1EC = models.FloatField()
    promI2EC = models.FloatField()
    promI3EC = models.FloatField()
    promI4EC = models.FloatField()
    promI5EC = models.FloatField()


    #Respuestas de la casa A FAVOR

    def calculopromIAF(self):
        rta1, rta2, rta3, rta4, rta5 = 0
        for i in self.get_players():
            rta1 = rta1 + i.I1AF
            rta2 = rta2 + i.I2AF
            rta3 = rta3 + i.I3AF
            rta4 = rta4 + i.I4AF
            rta5 = rta5 + i.I5AF

        rtasAF = []
        l = len(self.get_players())
        self.promI1AF = self.rta1/l
        self.promI2AF = self.rta2/l
        self.promI3AF = self.rta3/l
        self.promI4AF = self.rta4/l
        self.promI5AF = self.rta5/l

        rtasAF.append(self.promI1AF)
        rtasAF.append(self.promI2AF)
        rtasAF.append(self.promI3AF)
        rtasAF.append(self.promI4AF)
        rtasAF.append(self.promI5AF)

        return rtasAF

    # Respuestas de la casa ENCONTRA
    def calculopromIEC(self):
        rta1, rta2, rta3, rta4, rta5 = 0
        for i in self.get_players():
            rta1 = rta1 + i.I1EC
            rta2 = rta2 + i.I2EC
            rta3 = rta3 + i.I3EC
            rta4 = rta4 + i.I4EC
            rta5 = rta5 + i.I5EC

        rtasEC = []
        l = len(self.get_players())
        self.promI1EC = self.rta1/l
        self.promI2EC = self.rta2/l
        self.promI3EC = self.rta3/l
        self.promI4EC = self.rta4/l
        self.promI5EC = self.rta5/l

        rtasEC.append(self.promI1EC)
        rtasEC.append(self.promI2EC)
        rtasEC.append(self.promI3EC)
        rtasEC.append(self.promI4EC)
        rtasEC.append(self.promI5EC)

        return rtasEC

    def calcularCasaGanadora(self):
        promAF = sum(self.calculopromIAF())/len(self.calculopromIAF())
        promEC = sum(self.calculopromIEC())/len(self.calculopromIEC())

        return [promAF, promEC]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    I1AF = models.IntegerField(min=1,max=5)
    I2AF = models.IntegerField(min=1,max=5)
    I3AF = models.IntegerField(min=1,max=5)
    I4AF = models.IntegerField(min=1,max=5)
    I5AF = models.IntegerField(min=1,max=5)

    I1EC = models.IntegerField(min=1,max=5)
    I2EC = models.IntegerField(min=1,max=5)
    I3EC = models.IntegerField(min=1,max=5)
    I4EC = models.IntegerField(min=1,max=5)
    I5EC = models.IntegerField(min=1,max=5)