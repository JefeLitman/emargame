from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class encuesta(Page):
    form_model = 'player'
    form_fields = ['_id',
        'nombre',
        'edad',
        'carrera',
        'elecciones',
        'religion',
        'publico',
        'privado',
        'democratico',
        'ciudadana',
        'familiar',
        'corruptos',
        'sociedad',
        'exito',
        'sobornos',
        'necesidad',
        'mecanismos'
    ]

class gracias(Page):
    pass


page_sequence = [encuesta, gracias]
