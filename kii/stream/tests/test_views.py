from django.core.urlresolvers import reverse 

from . import base
from .. import models
from ..filterset import OwnerStreamItemFilterSet

class TestStreamViews(base.StreamTestCase):
    
    def test_base_stream_view_passes_current_stream_to_context(self):

        url = reverse('kii:stream:index')
        stream = models.Stream.objects.get(owner=self.users[0], title=self.users[0].username)
        self.login(self.users[0].username)
        response = self.client.get(url)

        self.assertEqual(response.context['current_stream'], stream)

    def test_anonymous_user_can_display_public_stream_item_detail_page(self):
        stream = models.Stream.objects.get(owner=self.users[0], title=self.users[0].username)
        si = models.StreamItem(root=stream, title="Hello", content="test", status="pub")
        si.save()
        stream.assign_perm('read', self.anonymous_user)

        url = si.reverse_detail()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], si)

    def test_stream_item_list_filter_class_change_depending_on_user(self):
        # anonymous see nothing
        stream = models.Stream.objects.get_user_stream(self.users[0])
        url = stream.reverse_detail()
        response = self.client.get(url)

        with self.assertRaises(KeyError):
            response.context['filterset']

        # log in as owner
        self.login(self.users[0].username)
        response = self.client.get(url)

        self.assertEqual(isinstance(response.context['filterset'],
                                    OwnerStreamItemFilterSet), True)
