"""
Django settings for TakedaAnalitic project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import socket
from .settings_db import DBHOST, DBNAME, DBPASSWORD, DBUSER

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd6nk=k26cj0r#*kf9pv%gjmgk@6vs9by9w0ud2g44aj^&9h6!0'

# SECURITY WARNING: don't run with debug turned on in production!
if socket.gethostname() == 'dsgate':
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1','192.168.7.5']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'debug_toolbar',
    'template_timings_panel',
    'db',
    'bi_base',
    'bi_auth',
    'widgetpages',
    'farmadmin',
    'dataloader',
]

if DEBUG:
    INSTALLED_APPS += ['django_celery_results']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TakedaAnalitic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bi_base.views.bi_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'TakedaAnalitic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': DBNAME,
        'USER': DBUSER,
        'PASSWORD': DBPASSWORD,
        'HOST': DBHOST,
        'PORT': '',

        'OPTIONS': {
            'driver': 'ODBC Driver 13 for SQL Server',
        },
    },
}

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'bimonitor-cache',
        }
    }

    CELERY_BROKER_URL = 'sqla+sqlite:///' + os.path.join(BASE_DIR, 'celery.db')
    CELERY_RESULT_BACKEND = 'django-db'
    CELERY_CACHE_BACKEND = 'default'

else:
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    #         'LOCATION': '127.0.0.1:11211',
    #     }
    # }
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            "KEY_PREFIX": "bimonitor"
        }
    }


    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
    CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
    CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
    CELERY_CACHE_BACKEND = 'default'

# set this to False if you want to turn off pyodbc's connection pooling
#DATABASE_CONNECTION_POOLING = False


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

STATICFILES_DIRS = [
    'assets',
]

MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/'

CSRF_USE_SESSIONS = True


BI_AUTH = True
BI_MAX_EMPLOYEE_LPU = 999
BI_MAX_EMPLOYEE_LOGIN = 10
BI_MAX_XLS_ROWS = 10000
BI_MAX_DOWNLOAD_ROWS = 15000
BI_TMP_FILES_DIR = os.path.join(BASE_DIR,'tmp')

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
    'SQL_WARNING_THRESHOLD': 100,  # milliseconds
}
