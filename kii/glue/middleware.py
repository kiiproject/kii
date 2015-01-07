# Aliasing it for the sake of page size.
from django.utils.html import strip_spaces_between_tags as short
from .utils import awesome_strip_spaces_between_tags

# from http://cramer.io/2008/12/01/spaceless-html-in-django/
# see this for preserving pygments (http://www.kd7eek.com/resources/software/python-django/middleware/)
class SpacelessMiddleware(object):
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = short(response.content)
            return response