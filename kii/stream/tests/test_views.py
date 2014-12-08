from django.core.urlresolvers import reverse 

from . import base
from .. import models


class TestStreamViews(base.StreamTestCase):
    
    def test_base_stream_view_passes_current_stream_to_context(self):

        url = reverse('kii:stream:index')
        stream = models.Stream.objects.get(owner=self.users[0], title=self.users[0].username)
        self.login(self.users[0].username)
        response = self.client.get(url)

        self.assertEqual(response.context['current_stream'], stream)