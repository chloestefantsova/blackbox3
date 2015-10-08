import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'XXX'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'slr1',
        'USER': 'slr1',
        'PASSWORD': 'XXX',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {
            'DB': 0,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            }
        },
    },
}


UPLOADED_TASK_DIR = os.path.join(BASE_DIR, 'uploaded_tasks')
UPLOADED_FILES_DIR = os.path.join(BASE_DIR, 'uploaded_files')
UPLOADED_IMAGES_DIR = os.path.join(BASE_DIR, 'uploaded_images')
UPLOADED_FILES_URL = '/files/'
UPLOADED_IMAGES_URL = '/images/'


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Novosibirsk'


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jury@school-ctf.org'
EMAIL_HOST_PASSWORD = 'XXX'
EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Recommended for development.
# WSGI_APPLICATION = 'ws4redis.django_runserver.application' # Development only.
