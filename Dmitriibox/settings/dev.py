from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%gmzr)1n3^6m=0w^0y@^5mewmjb4yn*b#j6#-(f=6uy4)dg&+r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# allowed host in VPS
ALLOWED_HOSTS = ['*', 'localhost']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

############ DEVUF TOOLBAR ###################
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Django Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

############ CHANNELS ###################
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

############## CORS #################
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# https://www.youtube.com/watch?v=A4SrKBLXg_Q
# https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://192.168.37.5:8080',
]