from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Lying_Survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    _id = models.StringField()
    nombre = models.StringField()
    edad = models.IntegerField(min=0, max=100)
    carrera = models.StringField()
    elecciones = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    religion = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    publico = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    privado = models.BooleanField(choices=[[True, 'Sí'], [False, 'No']])
    democratico = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    ciudadana = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    familiar = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    corruptos = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    sociedad = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    exito = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    sobornos = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    necesidad = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    mecanismos = models.LongStringField()

