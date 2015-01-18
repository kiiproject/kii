from django.conf import settings

import kii


def kii_metadata(request):
    return {
        'kii_version': kii.__version__,
        'kii_project_url': kii.PROJECT_URL,
    }

def tracking_code(request):
    return {
        'tracking_code': settings.TRACKING_CODE,
    }