from ...user.tests import base
from kii.tests.test_discussion import models
from django.db import IntegrityError
from ..models import AnonymousCommenterProfile


class CommentTestCase(base.UserTestCase):

    def test_comment_can_belong_to_user(self):
        c = self.G(models.DiscussionModelComment, user=self.users[0])

        self.assertEqual(c.user, self.users[0])

    def test_can_comment_discussion_model(self):
        
        m = self.G(models.DiscussionModel)
        c = self.G(models.DiscussionModelComment, subject=m, user=self.users[0])

        self.assertEqual(m.comments.all().first(), c)

    def test_comment_can_have_markdown_content(self):

        c = self.G(models.DiscussionModelComment, content="# nice", user=self.users[0])
        self.assertEqual(c.content.rendered, "<h1>nice</h1>")


    def test_comment_anonymous_comment_requires_username_and_email(self):

        m = self.G(models.DiscussionModel)
        p = self.G(AnonymousCommenterProfile, email="hello@me.com", username="something")
        c = models.DiscussionModelComment(subject=m)

        with self.assertRaises(IntegrityError):
            c.save()

        c.user_profile = p
        c.save()

    def test_comment_with_both_user_and_user_profile_raise_integrity_error(self):
        m = self.G(models.DiscussionModel)
        p = self.G(AnonymousCommenterProfile, email="hello@me.com", username="something")
        with self.assertRaises(IntegrityError):
            c1 = models.DiscussionModelComment(user_profile=p, user=self.users[0], subject=m)
            c1.save()

    def test_can_access_authenticated_and_anonymous_user_infos_with_the_same_api(self):
        m = self.G(models.DiscussionModel)
        p = self.G(AnonymousCommenterProfile, email="hello@me.com", username="something")
        c1 = self.G(models.DiscussionModelComment, user_profile=p)
        c2 = self.G(models.DiscussionModelComment, user=self.users[0])

        self.assertEqual(c1.profile.username, "something")
        self.assertEqual(c2.profile.username, self.users[0].username)

        self.assertEqual(c1.profile.email, "hello@me.com")
        self.assertEqual(c2.profile.email, self.users[0].email)

    def test_cannot_comment_if_dicussion_is_closed(self):
        m = self.G(models.DiscussionModel, discussion_open=False)
        c = models.DiscussionModelComment(subject=m, user=self.users[0])
        with self.assertRaises(ValueError):
            c.save()

    def test_comment_published_field_default_to_false_for_anonymous_users(self):
        
        p = self.G(AnonymousCommenterProfile, email="mail@me.com", username="something")
        m = self.G(models.DiscussionModel)
        c = self.G(models.DiscussionModelComment,subject=m, user_profile=p)

        self.assertEqual(c.published, False)

    def test_comment_published_field_default_true_for_authenticated_users(self):
        
        c = self.G(models.DiscussionModelComment, user=self.users[0])
        self.assertEqual(c.published, True)

    def test_can_hook_into_detect_unwanted(self):

        # see test_discussion/models.py for signal callback

        p = self.G(AnonymousCommenterProfile, email="hello@spam", username="something")
        m = self.G(models.DiscussionModel)
        c = models.DiscussionModelComment(subject=m, user_profile=p)
        c.save()
        self.assertEqual(c.unwanted, True)
        
    def test_unwanted_comment_default_to_published_false(self):

        m = self.G(models.DiscussionModel)
        c = self.G(models.DiscussionModelComment,subject=m, unwanted=True, user=self.users[0])

        self.assertEqual(c.published, False)







