"""
Django settings for slr1 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.utils.translation import ugettext_lazy as _


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django_extensions',
    'django_countries',
    'compressor',
    'ws4redis',
    'debug_toolbar',
    'debug_panel',

    'reg',
    'api',
    'game',
    'author',
)

MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.UpdateCacheMiddleware',
    'debug_panel.middleware.DebugPanelMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


ROOT_URLCONF = 'slr1.urls'

WSGI_APPLICATION = 'slr1.wsgi.application'


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


WEBSOCKET_URL = '/ws/'
WS4REDIS_PREFIX = 'ws'
def get_allowed_channels(request, channels):
    return set(channels).intersection(['subscribe-broadcast', 'subscribe-group'])
WS4REDIS_ALLOWED_CHANNELS = get_allowed_channels


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'ws4redis.context_processors.default',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

FILE_UPLOAD_HANDLERS = (
    'author.utils.TaskUploadHandler',
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.yuglify.YUglifyCSSFilter',
)

COMPRESS_JS_FILTERS = (
    'compressor.filters.yuglify.YUglifyJSFilter',
)

COMPRESS_PRECOMPILERS = (
    ('text/less',
     'lessc --global-var=\'STATIC_URL="%s"\' {infile} {outfile}' % STATIC_URL),
)


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
}


BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_PREFIX = 'session'


AUX_FILES_DIR = os.path.join(BASE_DIR, 'aux')


try:
    if os.getenv('platform') == 'heroku':
        from settings.heroku import *
    else:
        from settings.local import *
except Exception, ex:
    print ex
