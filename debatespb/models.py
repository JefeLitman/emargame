from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Alejandra Diaz & Valentina Mendoza'

doc = """
Hace falta generar la documentacion de la rubrica
"""


class Constants(BaseConstants):
    name_in_url = 'debatespb'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    promI1AG = models.FloatField()
    promI2AG = models.FloatField()
    promI3AG = models.FloatField()
    promI1AO = models.FloatField()
    promI2AO = models.FloatField()
    promI3AO = models.FloatField()
    promI1BG = models.FloatField()
    promI2BG = models.FloatField()
    promI3BG = models.FloatField()
    promI1BO = models.FloatField()
    promI2BO = models.FloatField()
    promI3BO = models.FloatField()
    promI1G = models.FloatField()
    promI2G = models.FloatField()
    promI3G = models.FloatField()
    promI4G = models.FloatField()



    #Respuestas de la casa Alta Gobierno

    def calculopromIAG(self):
        rta1, rta2, rta3 = 0, 0, 0
        for i in self.get_players():
            rta1 = rta1 + i.I1AG
            rta2 = rta2 + i.I2AG
            rta3 = rta3 + i.I3AG

        rtasAG = []
        l = len(self.get_players())
        self.promI1AG = float("{0:.2f}".format(rta1/l))
        self.promI2AG = float("{0:.2f}".format(rta2/l))
        self.promI3AG = float("{0:.2f}".format(rta3/l))


        rtasAG.append(self.promI1AG)
        rtasAG.append(self.promI2AG)
        rtasAG.append(self.promI3AG)

        return rtasAG

        # Respuestas de la casa Alta Oposición

    def calculopromIAO(self):
        rta1, rta2, rta3 = 0, 0, 0
        for i in self.get_players():
            rta1 = rta1 + i.I1AO
            rta2 = rta2 + i.I2AO
            rta3 = rta3 + i.I3AO

        rtasAO = []
        l = len(self.get_players())
        self.promI1AO = float("{0:.2f}".format(rta1 / l))
        self.promI2AO = float("{0:.2f}".format(rta2 / l))
        self.promI3AO = float("{0:.2f}".format(rta3 / l))

        rtasAO.append(self.promI1AO)
        rtasAO.append(self.promI2AO)
        rtasAO.append(self.promI3AO)

        return rtasAO

    # Respuestas de la casa BAJA GOBIERNO
    def calculopromIBG(self):
        rta1, rta2, rta3 = 0, 0, 0
        for i in self.get_players():
            rta1 = rta1 + i.I1BG
            rta2 = rta2 + i.I2BG
            rta3 = rta3 + i.I3BG

        rtasBG = []
        l = len(self.get_players())
        self.promI1BG = float("{0:.2f}".format(rta1/l))
        self.promI2BG = float("{0:.2f}".format(rta2/l))
        self.promI3BG = float("{0:.2f}".format(rta3/l))


        rtasBG.append(self.promI1BG)
        rtasBG.append(self.promI2BG)
        rtasBG.append(self.promI3BG)

        return rtasBG

    # Respuestas de la casa BAJA OPOSICION
    def calculopromIBO(self):
        rta1, rta2, rta3 = 0, 0, 0
        for i in self.get_players():
             rta1 = rta1 + i.I1BO
             rta2 = rta2 + i.I2BO
             rta3 = rta3 + i.I3BO

        rtasBO = []
        l = len(self.get_players())
        self.promI1BO = float("{0:.2f}".format(rta1/l))
        self.promI2BO = float("{0:.2f}".format(rta2/l))
        self.promI3BO = float("{0:.2f}".format(rta3/l))

        rtasBO.append(self.promI1BO)
        rtasBO.append(self.promI2BO)
        rtasBO.append(self.promI3BO)

        return rtasBO

    # Respuestas General
    def calculopromIG(self):
        rta1, rta2, rta3, rta4 = 0, 0, 0, 0
        for i in self.get_players():
            rta1 = rta1 + i.I1G
            rta2 = rta2 + i.I2G
            rta3 = rta3 + i.I3G
            rta4 = rta4 + i.I4G

        rtasG = []
        l = len(self.get_players())
        self.promI1G = float("{0:.2f}".format(rta1/l))
        self.promI2G = float("{0:.2f}".format(rta2/l))
        self.promI3G = float("{0:.2f}".format(rta3/l))
        self.promI4G = float("{0:.2f}".format(rta4/l))

        rtasG.append(self.promI1G)
        rtasG.append(self.promI2G)
        rtasG.append(self.promI3G)
        rtasG.append(self.promI4G)

        return rtasG

     #Calculo casa ganadora
    def calcularCasaGanadora(self):
        promAG = "{0:.2f}".format(sum(self.calculopromIAG())/len(self.calculopromIAG()))
        promAO = "{0:.2f}".format(sum(self.calculopromIAO())/len(self.calculopromIAO()))
        promBG = "{0:.2f}".format(sum(self.calculopromIBG())/len(self.calculopromIBG()))
        promBO = "{0:.2f}".format(sum(self.calculopromIBO())/len(self.calculopromIBO()))

        return [promAG, promAO, promBG, promBO]

    #Calculo debate general
    def calcularDebateGeneral(self):
        promG = "{0:.2f}".format(sum(self.calculopromIG())/len(self.calculopromIG()))

        return promG

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    I1AG = models.IntegerField()
    I2AG = models.IntegerField()
    I3AG = models.IntegerField()

    I1AO = models.IntegerField()
    I2AO = models.IntegerField()
    I3AO = models.IntegerField()

    I1BG = models.IntegerField()
    I2BG = models.IntegerField()
    I3BG = models.IntegerField()

    I1BO = models.IntegerField()
    I2BO = models.IntegerField()
    I3BO = models.IntegerField()

    I1G = models.IntegerField()
    I2G = models.IntegerField()
    I3G = models.IntegerField()
    I4G = models.IntegerField()