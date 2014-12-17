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

    def test_can_post_comment_as_logged_in_user(self):
        self.streams[0].assign_perm('read', self.anonymous_user)
        si = models.StreamItem(root=self.streams[0], title="test", status="pub")
        si.save()

        url = si.reverse_comment_create()

        self.login(self.users[0].username)
        response = self.client.post(url, {"content": "yolo"})

        self.assertEqual(si.comments.all().first().content.raw, "yolo")

    def test_can_post_comment_as_anonymous_user(self):
        self.streams[0].assign_perm('read', self.anonymous_user)
        si = models.StreamItem(root=self.streams[0], title="test", status="pub")
        si.save()

        url = si.reverse_comment_create()

        response = self.client.post(url, 
            {"username":"Edgar", "email":"contact@edgar.com", "content": "yolo"})

        comment = si.comments.all().first()
        self.assertEqual(comment.profile.username, "Edgar")
        self.assertEqual(comment.profile.email, "contact@edgar.com")