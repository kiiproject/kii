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

KII_APPS = (
    'base_models',
    'user',
    'app',
    'stream',
)
TEST_APPS = (
    'tests.test_base_models',
    'tests.test_user',
    'tests.test_app',
)

# Detect location and available modules
module_root = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
    AUTHENTICATION_BACKENDS = ['chrysalid.core.auth_backends.ChrysalidUserBackend',],
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django_nose',
    )+KII_APPS + TEST_APPS,
    KII_APPS=KII_APPS,
    SITE_ID = 1,    
    STATIC_URL = "/static/",
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ),
    TESTING=True,      
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ),
    TEST_RUNNER='django_nose.NoseTestSuiteRunner',
)

from django.test.utils import get_runner
TestRunner = get_runner(settings)

django.setup()
call_command('syncdb', verbosity=1, interactive=False)

# ---- app start
verbosity = 2 if '-v' in sys.argv else 1

runner = TestRunner(verbosity=verbosity, interactive=True, failfast=False)
failures = runner.run_tests(KII_APPS)

if failures:
    sys.exit(bool(failures))