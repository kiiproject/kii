

__version__ = "0.1"

APPS = (
    'kii.base_models',
    'kii.theme',
    'kii.hook',
    'kii.permission',
    'kii.user',
    'kii.app',
    'kii.stream',
    'kii.classify',
)


APPS_CONFIGS = ()

for app in APPS:
    APPS_CONFIGS += (".".join([app, "apps.App"]),)