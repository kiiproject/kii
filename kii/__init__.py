

__version__ = "0.1"

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