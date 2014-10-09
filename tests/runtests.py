#!/usr/bin/env python
from django.conf import settings, global_settings as default_settings
from django.core.management import call_command
import django
import sys
import os

# Give feedback on used versions
sys.stderr.write('Using Python version {0} from {1}\n'.format(sys.version[:5], sys.executable))
sys.stderr.write('Using Django version {0} from {1}\n'.format(
    django.get_version(),
    os.path.dirname(os.path.abspath(django.__file__)))
)
# Detect location and available modules
module_root = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KII_DIR = os.path.dirname(BASE_DIR)
sys.path.append(KII_DIR)

import kii

TEST_APPS = (
    'kii.tests.test_base_models',
    'kii.tests.test_user',
    'kii.tests.test_app',
    'kii.tests.test_app1',
    'kii.tests.test_app2',
    'kii.tests.test_theme',
    'kii.tests.test_permission',
    'kii.tests.templates',
)

TEST_APPS_FULL = ()

for app in TEST_APPS:
    TEST_APPS_FULL += (".".join([app, "apps.App"]),)


# Inline settings file
settings.configure(
    DEBUG = False, # will be False anyway by DjangoTestRunner.
    TEMPLATE_DEBUG = False,
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    TEMPLATE_CONTEXT_PROCESSORS = default_settings.TEMPLATE_CONTEXT_PROCESSORS + (
        'django.core.context_processors.request',
    ),
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django_nose',
        'guardian',
        'mptt',
    )+kii.APPS_CONFIGS + TEST_APPS_FULL,
    TEST_APPS=TEST_APPS,
    # kii settings
    KII_THEME="default",
    KII_APPS=kii.APPS,
    SITE_ID = 1,    
    STATIC_URL = "/static/",
    TEMPLATE_LOADERS = (
        'kii.theme.loaders.ThemeLoader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',

    ),
    TESTING=True,      
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ),
    TEST_RUNNER='django_nose.NoseTestSuiteRunner',

    # Guardian
    ANONYMOUS_USER_ID=-1,
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend', # this is default
        'guardian.backends.ObjectPermissionBackend',
    ),
    ROOT_URLCONF="kii.tests.urls",

    # group where all users will be registered. Used for permissions
    ALL_USERS_GROUP="all_users",
)

from django.test.utils import get_runner
TestRunner = get_runner(settings)

django.setup()
call_command('syncdb', verbosity=1, interactive=False)

# ---- app start
verbosity = 2 if '-v' in sys.argv else 1

runner = TestRunner(verbosity=verbosity, interactive=True, failfast=False)
apps_to_test = sys.argv[1:] or kii.APPS
failures = runner.run_tests(apps_to_test)

if failures:
    sys.exit(bool(failures))