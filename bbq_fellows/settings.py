from .django import *
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

DEBUG = True
LOGIN_REDIRECT_URL = 'events'