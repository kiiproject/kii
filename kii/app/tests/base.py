import django.test
from django.test import RequestFactory
from django_dynamic_fixture import G


class BaseTestCase(django.test.LiveServerTestCase):
    """A base Testcase other kii apps test cases inherit from"""    
    
    def G(self, model, **kwargs):
        """Shortcut for dynamic fixtures"""        
        return G(model, **kwargs)

    def setUp(self):
        self.factory = RequestFactory()

        super(BaseTestCase, self).setUp()

    def assertQuerysetEqualIterable(self, qs, it, **kwargs):

        r = [repr(e) for e in it]
        self.assertQuerysetEqual(qs, r, **kwargs)