"""
Django settings for superapp project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django.db.models.options as options
# from .database import POSTGRES_DATABASE
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y_nx76(#pe1u(qv-tifs!$v(w4d(ewa+2o@fjwl^*01-an@8g'


# Server's qualified domain name
try:
    from .root_local import LOCAL_SERVER_DOMAIN
except ImportError:
    pass
else:
    SERVER_DOMAIN = LOCAL_SERVER_DOMAIN

# Directive (in nginx configure file) to proxy pass to backend server.
BACKEND_PROXY_DIRECTIVE = "cctv_api"

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'backend-sneaker.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'api',
    'core',
    'rest_framework',
    'django.contrib.contenttypes',
    'django.contrib.auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


# DATABASES = {
#     'default': {},
#     'postgres_db': POSTGRES_DATABASE
# }

# Multi db:
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('using',)

DATABASE_ROUTERS = ['config.database_router.ModelMetaRouter']

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.base.base_apiView.customize_exception_handler',
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'
DB_TIMEZONE = 'Asia/Ho_Chi_Minh'

LANGUAGES = (
    ('vi', 'VietNam'),
    ('en', 'English'),
)

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = (
    '%d/%m/%Y', '%d/%m/%Y', '%d/%m/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',  # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
)

DATETIME_OUTPUT_FORMATS = '%Y-%m-%d %H:%M:%S'

DATETIME_FORMAT = 'd/m/Y H:i:s'
DATETIME_INPUT_FORMATS = (
    '%d/%m/%Y %H:%M:%S',  # '2006-10-25 14:30:59'
    '%d/%m/%Y %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%d/%m/%Y %H:%M',  # '2006-10-25 14:30'
)

YEAR_MONTH_FORMAT = '%b/%Y'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT= os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT= os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Mail
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'gsneaker118@gmail.com'
EMAIL_HOST_PASSWORD = 'Quang123'

DEFAULT_LANGUAGE_ID = 2

LAT = 16.088042
LON = 106.896973

DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5mb

DEBUG = True

django_heroku.settings(locals())
