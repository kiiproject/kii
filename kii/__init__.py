

# VERSION = (0, 8, 0, 'alpha', 0)
__version__ = '0.8'

PROJECT_URL = "http://code.eliotberriot.com/kii/kii"


APPS = (
    'kii.locale',
    'kii.hook',
    'kii.permission',
    'kii.user',
    'kii.api',
    'kii.glue',
    'kii.classify',
    'kii.search',
    'kii.file',
    'kii.stream',
    'kii.discussion',
    'kii.base_models',
    'kii.activity',
    'kii.app',
    'kii.vendor',
)


APPS_CONFIGS = ()

for app in APPS:
    APPS_CONFIGS += (".".join([app, "apps.App"]),)
