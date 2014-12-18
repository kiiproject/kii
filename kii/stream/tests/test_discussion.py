from django.core.urlresolvers import reverse

from kii.discussion.models import AnonymousCommenterProfile
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

    def test_moderation_page_require_to_be_stream_owner(self):

        s = models.Stream.objects.get(title=self.users[0].username, owner=self.users[0])
        url = reverse('kii:user_area:stream:itemcomment:moderation', kwargs={"username": self.users[0].username})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        self.login(self.users[0].username)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_moderation_return_correct_queryset(self):
        s = models.Stream.objects.get(title=self.users[1].username, owner=self.users[1])
        si0 = self.G(models.StreamItem, root=s)
        si1 = self.G(models.StreamItem)

        profile = self.G(AnonymousCommenterProfile)
        # comments 
        c0 = self.G(models.ItemComment, subject=si0, user_profile=profile)
        c1 = self.G(models.ItemComment, subject=si0, user_profile=profile)
        c2 = self.G(models.ItemComment, subject=si1, user_profile=profile)
        c3 = self.G(models.ItemComment, subject=si1, user_profile=profile)

        url = reverse('kii:user_area:stream:itemcomment:moderation', kwargs={"username": self.users[1].username})
        self.login(self.users[1].username)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqualIterable(response.context['object_list'], [c0, c1])
        self.assertEqual(response.context['can_moderate'], True)

    def test_set_status_view_require_stream_owner(self):
        s = models.Stream.objects.get(title=self.users[1].username, owner=self.users[1])
        si0 = self.G(models.StreamItem, root=s)
        c0 = self.G(models.ItemComment, subject=si0, user=self.users[0])

        url = reverse('kii:user_area:stream:itemcomment:set_status', 
            kwargs={"username": s.owner.username, "pk": c0.pk})+"?status=pub"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.login(self.users[1].username)
        response = self.client.get(url)

        c = models.ItemComment.objects.get(pk=c0.pk)
        self.assertEqual(c.status, "pub")