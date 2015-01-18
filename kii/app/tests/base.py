import django.test
from django.test import RequestFactory
from django_dynamic_fixture import G
from django.contrib.sites.models import get_current_site
from bs4 import BeautifulSoup
from kii.utils import full_url

class BaseTestCase(django.test.LiveServerTestCase):
    """A base Testcase other kii apps test cases inherit from"""

    def setup(self):
        """Update site url for absolute url building"""
        domain = "{0}:{1}".format(
            self.server_thread.host, 
            self.server_thread.port
        )
        site = get_current_site(None)
        site.domain = domain
        site.save()

    def G(self, model, **kwargs):
        """Shortcut for dynamic fixtures"""
        return G(model, **kwargs)

    def setUp(self):
        self.factory = RequestFactory()

        super(BaseTestCase, self).setUp()

    def full_url(self, *args, **kwargs):
        return full_url(*args, **kwargs)

    def assertQuerysetEqualIterable(self, qs, it, **kwargs):

        r = [repr(e) for e in it]
        self.assertQuerysetEqual(qs, r, **kwargs)

    def parse_html(self, html):
        """Return a BeaufifulSoup object with parsed HTML"""
        return BeautifulSoup(html)
