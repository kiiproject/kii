from markdown import inlinepatterns, util, Extension

from django.core.urlresolvers import reverse

USERNAME_RE = r'(@[\w@+-]+)'


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


class KiiFlavoredMarkdownExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["username"] = UsernamePattern(USERNAME_RE)


def makeExtension(*args, **kwargs):
    return KiiFlavoredMarkdownExtension(*args, **kwargs)
