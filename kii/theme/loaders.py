from django.template.loaders import app_directories
from django.conf import settings

class ThemeLoader(app_directories.Loader):
    """Will try to load templates from within theme directory"""

    def get_template_sources(self, template_name, template_dirs=None):
        
        template_name = settings.KII_THEME + "/" + template_name
        return super(ThemeLoader, self).get_template_sources(template_name, template_dirs)
