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
    codigo = models.StringField()
    carrera = models.StringField()
    semestre = models.IntegerField()
    pga = models.StringField()
    edad = models.IntegerField(min=0, max=100)
    sexo = models.BooleanField(choices=[[True, 'M'], [False, 'F']])
    estrato = models.IntegerField(choices=[1, 2, 3, 4, 5, 6])
    religion = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    elecciones = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    publico = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    privado = models.BooleanField(choices=[[True, 'Sí'], [False, 'No']])
    familiar = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    exito = models.BooleanField(choices=[[True, 'Si'], [False, 'No']])
    Multinacional = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    negocio = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    empleado = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    consultoria = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    sectorfinanciero = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    glocal = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    organizacion = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    gnacional = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    gdepartamental = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    copia = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    beca = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)
    celular = models.IntegerField(choices=[1,2,3,4,5,6,7,8,9,10], widget=widgets.RadioSelectHorizontal)

