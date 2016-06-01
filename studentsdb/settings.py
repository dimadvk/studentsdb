"""
Django settings for studentsdb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from django.conf import global_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ye#_i*tty*u53sqpy1l=9dkqszm+-n#(6lbqh@*8vepfp&^8zj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['studentsdb.local', 'studentsdb.uk.to']

TEMPLATE_DEBUG = True


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'registration',
    'social.apps.django_app.default',
    'django_coverage',
    'students',
    'stud_auth',
#    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'studentsdb.middleware.RequestTimeMiddleware',
    'studentsdb.middleware.SqlQueriesTimeMiddleware',
    'studentsdb.middleware.LocalizeStaticMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# for crispy_forms...
CRISPY_TEMPLATE_PACK = 'bootstrap3'
#

ROOT_URLCONF = 'studentsdb.urls'

WSGI_APPLICATION = 'studentsdb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

from .db import DATABASES

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'uk'

USE_TZ = True
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    "social.apps.django_app.context_processors.backends",
    "studentsdb.context_processors.students_proc",
    "django.contrib.messages.context_processors.messages",
    "students.context_processors.groups_processor",
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.vk.VKOAuth2',
)
SOCIAL_AUTH_FACEBOOK_KEY = '542329375940973'
SOCIAL_AUTH_FACEBOOK_SECRET = '36b075370d6f7e06ac4d225d3d2d3f6d'
SOCIAL_AUTH_TWITTER_KEY = '3fOvNasLOBr3vz0qsWDfI1uaX'
SOCIAL_AUTH_TWITTER_SECRET = 's0OvZEnEN0pfXVwYjUQxRhp00zPwMzOImjzxbDu2bNIIv0szst'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '240649527890-d6rbb1stb0ie7su6far0n8hf391qqsnu.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'cFNOhKr97kUKwu0zILkFD2Hx'
SOCIAL_AUTH_VK_OAUTH2_KEY = '5387686'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'qUslkggkHce9NjkGTrhx'

# for 'registration' app 
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 1
REGISTRATION_FORM = 'stud_auth.forms.CustomRegForm'
#PORTAL_URL = 'http://localhost:8000'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'students', 'templates', 'students'),
    os.path.join(BASE_DIR, 'stud_auth', 'templates'),
)

LOGIN_URL = 'users:auth_login'
LOGOUT_URL = 'users:auth_logout'
LOGIN_REDIRECT_URL = 'home'

# email settings
ADMIN_EMAIL = "ren-kpi@i.ua"
ADMINS = (
    ('admin', 'ren-kpi@i.ua'),
)
from .smtp_settings import *
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = 'email_files'
SERVER_EMAIL = "dvk@skif.net.ua"
DEFAULT_FROM_EMAIL = "dvk@skif.net.ua"

# as django-contact-form needs
MANAGERS = [
    ('admin', 'ren-kpi@i.ua'),
]

# for localize static management command and LocalizeStaticMiddleware 
LOCALIZE_STATIC = {
    'app_name': 'students',
    'static_css_dir': 'css',
    'static_js_dir': 'js'
}


# messages - storage backend
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# for 'registration' app
REFISTRATION_OPEN = True

# for test_coverage command
COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'coverage') 

# debug_toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = True
INSTALLED_APPS += ('django_jenkins',)
JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                 'django_jenkins.tasks.run_pep8',
                 'django_jenkins.tasks.run_pyflakes',)

# logging settings
LOG_FILE = os.path.join(BASE_DIR, 'studentsdb.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose',
            'filters': ['require_debug_false'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins', 'file', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'students.signals': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            #'propagate': False,
        },
        'students.views.contact_admin': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
        },
    }
}


# for jenkins
current_user = os.getenv('USER')
if current_user == 'jenkins':
    import imp
    # load db settings
    imp.load_source('db_settings',
        '/data/work/virtualenvs/studentsdb/src/studentsdb/studentsdb/db.py')
    from db_settings import DATABASES
    # load smtp settings
    imp.load_source('smtp_settings',
        '/data/work/virtualenvs/studentsdb/src/studentsdb/studentsdb/smtp_settings.py')
    from smtp_settings import *
    # set MEDIA_ROOT
    #MEDIA_ROOT = '/data/work/virtualenvs/studentsdb/src/media'
