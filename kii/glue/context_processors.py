import kii


def kii_metadata(request):
    """TODO : is user_access really needed ?"""
    return {
        'kii_version': kii.__version__,
        'kii_project_url': kii.PROJECT_URL,
    }
