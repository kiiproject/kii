from ...user.tests import base
from kii.tests.test_discussion import models

class CommentTestCase(base.UserTestCase):

    def test_can_comment_discussion_model(self):
        
        m = self.G(models.DiscussionModel)
        c = self.G(models.DiscussionModelComment, subject=m)

        self.assertEqual(m.comments.all().first(), c)

    def test_comment_can_have_markdown_content(self):

        c = self.G(models.DiscussionModelComment, content="# nice")
        self.assertEqual(c.content.rendered, "<h1>nice</h1>")