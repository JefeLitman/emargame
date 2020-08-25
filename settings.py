from os import environ

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
        'name':'debatespb',
        'display_name': 'Evaluación Debate Parlamento Británico',
        'num_demo_participants':1,
        'app_sequence': ['debatespb'],
        'Rounds':None,
        'ConSin':None,
        'doc':"""
        """
    },
    {
        'name':'DataMental_Exp_Session',
        'display_name': 'Juego de la Mentira',
        'num_demo_participants':1,
        'app_sequence': ['DataMental_Exp','DataMental_Sur'],
        'doc':"""
        """
    }

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'COP'
USE_POINTS = True

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
        'name': 'debatepb',
        'display_name': 'Sala de evaluación Debate Parlamento Británico',
    },
    {
        'name': 'datamental',
        'display_name': 'Juego de la Mentira',
    }
]

if(environ.get('OTREE_ADMIN_PASSWORD')==None):
    ADMIN_USERNAME = 'admin'
    environ['OTREE_ADMIN_PASSWORD'] = '1234'
else:
    ADMIN_USERNAME = 'EmarLab'

ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# for security, best to set admin password in an environment variable
environ['OTREE_PRODUCTION'] = '1'
environ['OTREE_AUTH_LEVEL'] = 'DEMO'
#0 Para no tenerlo en producción y DEBUG
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

if(environ.get('OTREE_SYSTEM') != None):
    environ["DATABASE_URL"]='postgres://emar:123456@localhost/emar_db'

DEMO_PAGE_INTRO_HTML = """ Juegos EMAR LAB """

SECRET_KEY = '*u-oae#nou+$tqkvqs30lz89r=48+_o*7+b8jkm=*&4v5+&tn8'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']