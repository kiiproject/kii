from ...user.tests import base
from kii.tests.test_discussion import models
from django.db import IntegrityError

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
        c = models.DiscussionModelComment(subject=m)

        with self.assertRaises(IntegrityError):
            c.save()

        c.username = "something"
        c.email = "hello@me.com"

        c.save()


