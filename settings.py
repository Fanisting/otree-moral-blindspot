from os import environ
import os 

SESSION_CONFIGS = [
    dict(
        name='mind_game',
        app_sequence=['mind_game'],
        num_demo_participants=3,
    ),
    dict(
        name='mindgame_uncertain',
        app_sequence=['mindgame_uncertain'],
        num_demo_participants=3,
    ),
    dict(
        name='mindgame_base_uncertain',
        app_sequence=['Consent', 'mind_game', 'mindgame_uncertain', 'survey'],
        num_demo_participants=3,
        # use_browser_bots=True,
    ),
    dict(
        name='mindgame_watch_AI',
        app_sequence=['Consent', 'mindgame_watch', 'mindgame_AI', 'survey'],
        num_demo_participants=3,
    ),
    dict(
        name='mindgame_watch',
        app_sequence=['mindgame_watch',],
        num_demo_participants=3,
    ),
    dict(
        name='mindgame_AI',
        app_sequence=['mindgame_AI',],
        num_demo_participants=3,
    ),
    dict(
        name='survey',
        app_sequence=['survey',],
        num_demo_participants=3,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.266, participation_fee=4.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5965256070818'

#No Debugging
DEBUG = False

