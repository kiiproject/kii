

def full_url(path):
    """Return a full URL, with protocol and domain"""
    
    from django.contrib.sites.models import get_current_site
    request = None
    return ''.join(['http://', get_current_site(request).domain, path])
