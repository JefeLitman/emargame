import os
from os import environ

import dj_database_url

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
environ.__setitem__('OTREE_PRODUCTION','1') ################
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

if(environ.get('OTREE_ADMIN_PASSWORD')==None):
    ADMIN_USERNAME = 'admin'
    environ.__setitem__('OTREE_ADMIN_PASSWORD','123456')
else:
    ADMIN_USERNAME = 'EmarLab'

ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# don't share this with anybody.
SECRET_KEY = '6b%cfzhh9ab%=-!&l#miwv$oa%q@m9j%7nanw!laq4u*q$mlzz'

if(environ.get('OTREE_SYSTEM')!=None):
    environ.__setitem__('DATABASE_URL','postgres://emar:123456@localhost/emar_db')
    DATABASES = {
        'default': dj_database_url.config(
            #default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')########################
        )
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')########################3
        )
    }

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

environ.__setitem__('OTREE_AUTH_LEVEL','DEMO') ###########
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'COP'
USE_POINTS = True


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'es'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
Juegos EMAR LAB
"""

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'participation_fee': 0,
    'real_world_currency_per_point': 1,
    'Rounds':10,
    'ConSin':False,
    'doc':"""
    Rounds: Número total de periodos que se jugarán. Por defecto en 10 y maximo 20.<br/>
    ConSin: Tomará el valor de 1 cuando los periodos iniciales son tratamiento con revisión y los periodos finales sin revisión. En caso contrario será 0. Por defecto 0 (Sin marcar).
    """
}
# anything you put after the below line will override
# oTree's default settings. Use with caution.
SESSION_CONFIGS = [
    {
        'name':'debates',
        'display_name': 'Evaluacion del Debate',
        'num_demo_participants':1,
        'app_sequence': ['debates'],
        'Rounds':None,
        'ConSin':None,
        'doc':"""
        """
    },
    {
        'name':'mercados_prohibidos',
        'display_name':'1. Mercados Prohibidos: Regulación y disuasión.',
        'num_demo_participants':2,
        'app_sequence': ['mercados_prohibidos']
    },
    {
        'name': 'garrote_zanahoria',
        'display_name': '2. Garrote & Zanahoria: Normas sociales y mecanismos de cumplimiento.',
        'num_demo_participants': 2,
        'app_sequence': ['garrote_zanahoria'],
        'ConSin':None,
        'MasMenos':False,
        'doc':"""
        Rounds: Número total de periodos que se jugarán. Por defecto en 10 y maximo 20.<br/>
        MasMenos: Tomará el valor de 1 cuando los periodos iniciales son tratamiento zanahoria y los periodos finales garrote. En caso contrario será 0. Por defecto 0 (Sin marcar).
        """
    },
    {
        'name': 'inversion_coordinacion_reputacion',
        'display_name': '3. Inversión: Coordinación y reputación.',
        'num_demo_participants': 2,
        'app_sequence': ['inversion_coordinacion_reputacion']
    },
    {
        'name':'confianza',
        'display_name': '4. Confianza: Identidad de grupo y cooperación.',
        'num_demo_participants': 2,
        'app_sequence': ['confianza']
    },
    {
        'name': 'conflicto',
        'display_name': '5. Conflicto 2x2: Negociar como halcón o como paloma.',
        'num_demo_participants': 2,
        'app_sequence': ['conflicto'],
        'ConSin':None,
        'SecSim':False,
        'doc':"""
        Rounds: Número total de periodos que se jugarán. Por defecto en 10 y maximo 20.<br/>
        SecSim:  Tomará el valor de 1 cuando los periodos iniciales son tratamiento secuencial y los periodos finales simultaneo. En caso contrario será 0. Por defecto 0 (Sin marcar).
        """
    },
    {
        'name':'signals',
        'display_name': '6. Señales: Interpretación y manipulación de la información.',
        'num_demo_participants':2,
        'app_sequence': ['signals']
    },
    {
        'name':'buscadores_renta',
        'display_name': '7. Buscadores de rentas: Competencia y pérdidas de eficiencia.',
        'num_demo_participants':2,
        'app_sequence': ['buscadores_renta'],
        'ConSin':None,
        'LotSub':False,
        'doc':"""
        Rounds: Número total de periodos que se jugarán. Por defecto en 10 y maximo 20.<br/>
        LotSub:  Tomará el valor de 1 cuando los periodos iniciales son tratamiento loteria y los periodos finales subasta. En caso contrario será 0. Por defecto 0 (Sin marcar).
        """
    },
    {
        'name':'paradoja_votante',
        'display_name': '8. Paradoja del votante: Voto pivote y abstención.',
        'num_demo_participants':2,
        'app_sequence': ['paradoja_votante']
    },
    {
        'name':'corrupcion_malversacion',
        'display_name': 'Juego de la Malversacion',
        'num_demo_participants':15,
        'app_sequence': ['corrupcion_malversacion'],
        'Rounds':1,
        'ConSin':None,
        'doc':"""
        Rounds: Número total de periodos que se jugarán (Maximo 10). Por defecto en 1.
        """
    },
    {
        'name':'debatespb',
        'display_name': 'Evaluación Debate Parlamento Británico',
        'num_demo_participants':1,
        'app_sequence': ['debatespb'],
        'Rounds':None,
        'ConSin':None,
        'doc':"""
        """
    }
]

#oTree ROOMS
ROOM_DEFAULTS = {
    'participant_label_file':'labels.txt',
    'use_secure_urls': False
}

ROOMS = [
{
        'name': 'debate',
        'display_name': 'Sala de evaluación  del debate',
    },
    {
        'name': 'mercados',
        'display_name': 'Sala del juego Mercados Prohibidos',
    },
    {
        'name': 'garrote',
        'display_name': 'Sala del juego Garrote y Zanahoria'
    },
    {
        'name': 'inversion',
        'display_name': 'Sala del juego Inversion: Coordinacion y Reputacion'
    },
    {
        'name': 'confianza',
        'display_name': 'Sala del juego Confianza'
    },
    {
        'name': 'conflicto',
        'display_name': 'Sala del juego Conflicto 2x2'
    },
    {
        'name': 'senales',
        'display_name': 'Sala del juego Señales'
    },
    {
        'name': 'renta',
        'display_name': 'Sala del juego Buscadores de Renta'
    },
    {
        'name': 'votante',
        'display_name': 'Sala del juego Paradoja del Votante'
    },
    {
        'name': 'malversacion',
        'display_name': 'Sala del juego de la Malversacion'
    },
    {
        'name': 'debatepb',
        'display_name': 'Sala de evaluación Debate Parlamento Británico',
    }
]

otree.settings.augment_settings(globals())
