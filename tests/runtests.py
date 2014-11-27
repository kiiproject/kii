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
    'kii.tests.test_stream',
    'kii.tests.test_discussion',
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
        'kii.app.context_processors.user_apps',
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
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django_nose',
        'guardian',
        "compressor",
        "djangobower",
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
        'kii.theme.finders.ThemeFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
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
    LOGIN_REDIRECT_URL="kii:stream:index",
    LOGGING= {
        'version': 1,
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers':['console'],
                'propagate': True,
                'level':'DEBUG',
            }, 
        },  
    },

    # Bower

    BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, "components"),
    BOWER_INSTALLED_APPS = (
        "foundation",
    ),
    # Compressor
    # If compressor does not work, ensure you have compass installed (gem install compass)
    COMPRESS_ENABLED = True,
    COMPRESS_PARSER = 'compressor.parser.LxmlParser',
    COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter'],
    COMPRESS_JS_FILTERS = [],
    COMPRESS_OFFLINE = True,
    # in case of emergency, refer to http://stackoverflow.com/questions/20559698/django-bower-foundation-5-sass-how-to-configure
    COMPRESS_PRECOMPILERS = (
        ('text/x-scss', 'sass --scss --compass -I "{0}/bower_components/foundation/scss" "{infile}" "{outfile}"'.format(os.path.join(BASE_DIR, "components"), infile="{infile}", outfile="{outfile}")),
    ),
    STATIC_ROOT=os.path.join(BASE_DIR, "static")

)

from django.test.utils import get_runner
TestRunner = get_runner(settings)


django.setup()

from djangobower.management.commands.bower_install import Command as bower_install

b = bower_install()
b.execute()
call_command('syncdb', verbosity=1, interactive=False)
call_command('compress', verbosity=1, interactive=False, force=True)

# ---- app start
verbosity = 2 if '-v' in sys.argv else 1

runner = TestRunner(verbosity=verbosity, interactive=True, failfast=False)
functional = len(sys.argv) > 0 and "_functional" == sys.argv[-1]

argv = sys.argv[1:]

if functional:
    # exclude functional param 
    argv = sys.argv[1:-1]

apps_to_test = argv or kii.APPS
if functional:
    apps_to_test = ["{0}.tests.functional_tests".format(app_name) for app_name in apps_to_test]
failures = runner.run_tests(apps_to_test)

if failures:
    sys.exit(bool(failures))