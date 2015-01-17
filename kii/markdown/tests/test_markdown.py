from django.conf import settings
from django.core.urlresolvers import reverse

from kii.stream.tests.base import StreamTestCase
from .. import inlinepatterns

markdown = settings.MARKDOWN_FUNCTION


class TestMarkdown(StreamTestCase):


    def test_markdown_can_reference_user(self):
        """test the @username syntax"""
        username = self.users[0].username
        content = "@{0}".format(username)
        rendered = markdown(content)
        expected = """<p><a href="{0}">@{1}</a></p>""".format(
                    reverse("kii:user_area:user:profile",
                            kwargs={"username": username}),
                    username)

        self.assertEqual(rendered, expected)

        