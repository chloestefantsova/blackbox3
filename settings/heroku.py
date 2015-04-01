import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '14bc29163d1d900d577df46dfb192eaa6d2ceb72'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {'default':  dj_database_url.config()}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Novosibirsk'
