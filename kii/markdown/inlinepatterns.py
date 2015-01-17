from markdown import inlinepatterns, util, Extension

from django.core.urlresolvers import reverse

USERNAME_RE = r'(@[\w@+-]+)'
STREAM_RE = r'#(stream)\/([\w@+-_]+)'
ITEM_RE = r'#(item)\/([\w@+-_]+)'


class UsernamePattern(inlinepatterns.Pattern):

    def handleMatch(self, m):
        # keep the username without @
        username = m.group(2)[1:]
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return m.group(2)

        user_profile_url = reverse("kii:user_area:user:profile",
                                   kwargs={"username": user.username})
        el = util.etree.Element("a")
        el.set('href', user_profile_url)
        el.text = m.group(2)

        return el


class HashPattern(inlinepatterns.Pattern):

    def get_model(self):
        raise NotImplementedError

    def get_object(self):
        raise NotImplementedError

    def get_identifier(self, string):
        return string

    def handleMatch(self, m):

        pattern = "#{0}/{1}".format(self.contenttype, m.group(3))

        try:
            identifier = self.get_identifier(m.group(3))
        except ValueError:
            return pattern
        try:
            target = self.get_object(identifier)
        except self.get_model().DoesNotExist:
            return pattern

        el = util.etree.Element("a")
        el.set('href', target.get_absolute_url())
        el.text = pattern
        return el


class StreamHashPattern(HashPattern):

    contenttype = "stream"

    def get_model(self):
        from kii.stream import models
        return models.Stream

    def get_object(self, identifier):
        return self.get_model().objects.get(slug=identifier)


class ItemHashPattern(HashPattern):
    contenttype = "item"

    def get_identifier(self, string):
        return int(string)

    def get_model(self):
        from kii.stream import models
        return models.StreamItem

    def get_object(self, identifier):
        return self.get_model().objects.get(pk=identifier)


class KiiFlavoredMarkdownExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["username"] = UsernamePattern(USERNAME_RE)
        md.inlinePatterns["kii_stream"] = StreamHashPattern(STREAM_RE)
        md.inlinePatterns["kii_stream_item"] = ItemHashPattern(ITEM_RE)


def makeExtension(*args, **kwargs):
    return KiiFlavoredMarkdownExtension(*args, **kwargs)
