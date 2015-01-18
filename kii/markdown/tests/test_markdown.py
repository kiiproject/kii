from django.conf import settings
from django.core.urlresolvers import reverse

from kii.stream.tests.base import StreamTestCase
from kii.stream import models



markdown = settings.MARKDOWN_FUNCTION


class TestMarkdown(StreamTestCase):


    def test_markdown_can_reference_user(self):
        """test the @username syntax"""
        username = self.users[0].username
        content = "@{0}".format(username)
        rendered = markdown(content)
        expected = """<p><a href="{0}">@{1}</a></p>""".format(
                    self.full_url(reverse("kii:user_area:user:profile",
                            kwargs={"username": username})),
                    username)

        self.assertEqual(rendered, expected)

    def test_markdown_can_reference_stream(self):
        """test the #stream/slug syntax"""
        stream = self.streams[0]
        slug = stream.slug

        content = "Test #stream/{0}".format(slug)
        rendered = markdown(content)
        expected = """<p>Test <a href="{0}">{1}</a></p>""".format(
                    self.full_url(reverse("kii:stream:stream:index",
                            kwargs={"stream": slug})),
                    "#stream/{0}".format(slug))

        self.assertEqual(rendered, expected)

    def test_markdown_can_reference_item(self):
        """test the #item/pk syntax"""
        stream = self.streams[0]
        i = models.StreamItem(title="Hello", root=stream)  
        i.save()
        content = "Test #item/{0}".format(i.pk)
        rendered = markdown(content)
        expected = """<p>Test <a href="{0}">{1}</a></p>""".format(
                    self.full_url(reverse("kii:stream:stream:streamitem:detail",
                            kwargs={"pk": i.pk, "stream": i.root.slug})),
                    "#item/{0}".format(i.pk))

        self.assertEqual(rendered, expected)

    def test_hash_pattern_accepts_anchor(self):
        stream = self.streams[0]
        slug = stream.slug

        content = "Test #stream/{0}(yolo)".format(slug)
        rendered = markdown(content)
        expected = """<p>Test <a href="{0}">yolo</a></p>""".format(
                    self.full_url(reverse("kii:stream:stream:index",
                            kwargs={"stream": slug})))

        self.assertEqual(rendered, expected)