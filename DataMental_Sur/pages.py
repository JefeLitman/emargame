from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class encuesta(Page):
    form_model = 'player'
    form_fields = ['codigo', 
        'carrera', 
        'semestre', 
        'pga', 
        'edad', 
        'sexo', 
        'estrato', 
        'religion', 
        'elecciones', 
        'publico', 
        'privado', 
        'familiar', 
        'exito',
        'Multinacional', 
        'negocio', 
        'empleado', 
        'sectorfinanciero', 
        'consultoria', 
        'glocal', 
        'organizacion', 
        'gnacional', 
        'gdepartamental', 
        'copia', 
        'beca', 
        'celular'
    ]

class gracias(Page):
    pass


page_sequence = [encuesta, gracias]
