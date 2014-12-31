#!/usr/bin/env python
from django.conf import settings
from django.core.management import call_command
import django
import sys
import os

# Give feedback on used versions
sys.stderr.write('Using Python version {0} from {1}\n'.format(sys.version[:5],
                                                              sys.executable))
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
from kii.tests import settings as test_settings
# Inline settings file
settings.configure(
    test_settings,
    INSTALLED_APPS=test_settings.INSTALLED_APPS + (
        'django_nose',
    )
)

from django.test.utils import get_runner
TestRunner = get_runner(settings)

django.setup()

# from djangobower.management.commands.bower_install import Command as bower_install

# b = bower_install()
# b.execute()
call_command('syncdb', verbosity=1, interactive=False)
#call_command('compress', verbosity=1, interactive=False, force=True)

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
    apps_to_test = [
        "{0}.tests.functional_tests".format(app_name)
        for app_name in apps_to_test
    ]
failures = runner.run_tests(apps_to_test)

if failures:
    sys.exit(bool(failures))
