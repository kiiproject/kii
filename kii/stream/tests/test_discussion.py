from django.core.urlresolvers import reverse

from . import base
from .. import models



class TestDiscussion(base.StreamTestCase):
    
    def test_can_attach_comments_to_stream_items(self):

        si = models.StreamItem(root=self.streams[0], title="test", status="pub")
        si.save()

        c = models.ItemComment(subject=si, user=self.users[1], content="Hello world")
        c.save()

        self.assertEqual(si.comments.all().first(), c)

