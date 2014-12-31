from django.utils.version import get_version

VERSION = (0, 2, 0, 'alpha', 0)
__version__ = get_version(VERSION)


APPS = (
    'kii.locale',
    'kii.hook',
    'kii.permission',
    'kii.user',
    'kii.api',
    'kii.glue',
    'kii.classify',
    'kii.stream',
    'kii.discussion',
    'kii.base_models',
    'kii.app',
)


APPS_CONFIGS = ()

for app in APPS:
    APPS_CONFIGS += (".".join([app, "apps.App"]),)
