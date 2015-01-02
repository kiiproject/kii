"""Base settings shared by all environments"""
# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *  # NOQA
from django.core.urlresolvers import reverse_lazy
#from https://github.com/lincolnloop/django-layout/blob/master/project_name/settings/base.py

import os
import kii

KII_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'kii.app.context_processors.user_apps',
    'kii.stream.context_processors.user_stream',
    'kii.stream.context_processors.item_models',
    'kii.glue.context_processors.kii_metadata',
    'kii.glue.context_processors.tracking_code',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'kii.base_models.middleware.OwnerMiddleware',
    #'kii.glue.middleware.SpacelessMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'guardian',
    'polymorphic',
    'django_filters',
    'mptt',
    'rest_framework',
) + kii.APPS_CONFIGS

# kii settings

KII_APPS = kii.APPS

# group where all users will be registered. Used for permissions
ALL_USERS_GROUP = "all_users"


LOCALE_PATHS += (
    os.path.join(KII_DIR, "locale"),
)

SITE_ID = 1
STATIC_URL = "/static/"
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Guardian
ANONYMOUS_USER_ID = -1
AUTHENTICATION_BACKENDS += (
    'guardian.backends.ObjectPermissionBackend',
)

LOGIN_URL = "kii:user:login"
REVERSED_LOGIN_URL = reverse_lazy(LOGIN_URL)
LOGIN_REDIRECT_URL = "kii:stream:index"

# localization

TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

from django.utils.functional import curry
import markdown
from markdown.extensions.codehilite import makeExtension as CodeHilite # noqa

md_filter = curry(markdown.markdown, extensions=[CodeHilite(css_class='code',
                                                            linenums=False, 
                                                            noclasses=True)])
MARKDOWN_FUNCTION = md_filter

#markupfield
MARKUP_FIELD_TYPES = (
    ('markdown', md_filter),
    ('none', lambda s: s),
)

# Tracking code (like Piwik or Google Analytics) that will be included in every template
TRACKING_CODE = ""

