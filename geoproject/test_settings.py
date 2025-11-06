from .settings import *
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'test_geodjango_db',  
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'postgres'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5433'),
        'TEST': {
            'NAME': 'test_geodjango_db',  
        }
    }
}











DEBUG = False


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]











LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',  
    },
}


EMAIL_BACKEND = 'django.core.mail.backends.localmemory.EmailBackend'


MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')


STATIC_ROOT = os.path.join(BASE_DIR, 'test_static')


for template in TEMPLATES:
    template['OPTIONS']['debug'] = True


REST_FRAMEWORK['TEST_REQUEST_DEFAULT_FORMAT'] = 'json'
REST_FRAMEWORK['TEST_REQUEST_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}



