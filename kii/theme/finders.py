from django.contrib.staticfiles.finders import AppDirectoriesFinder
from django.conf import settings

class ThemeFinder(AppDirectoriesFinder):
    """Will prefix requested static file path with current theme"""

    def find(self, path, **kwargs):
        path = settings.KII_THEME + "/" + path
        return super(ThemeFinder, self).find(path, **kwargs)
