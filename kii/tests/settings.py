#!/usr/bin/env python
from kii.glue.common_settings import *
import kii

TEST_APPS = (
    'kii.tests.test_base_models',
    'kii.tests.test_user',
    'kii.tests.test_api0',
    'kii.tests.test_api1',
    'kii.tests.test_app',
    'kii.tests.test_app1',
    'kii.tests.test_app2',
    'kii.tests.test_permission',
    'kii.tests.templates',
    'kii.tests.test_stream',
    'kii.tests.test_discussion',
)

TEST_APPS_FULL = ()

for app in TEST_APPS:
    TEST_APPS_FULL += (".".join([app, "apps.App"]),)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS += TEST_APPS_FULL

TESTING=True    

TEST_RUNNER='django_nose.NoseTestSuiteRunner'

ROOT_URLCONF="kii.tests.urls"

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
}


# let's speed up the tests

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

import logging

logging.disable(logging.ERROR)
DEBUG = False
TEMPLATE_DEBUG = False
MIGRATION_MODULES = DisableMigrations()
