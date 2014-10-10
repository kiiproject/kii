from markupfield.fields import MarkupField as MKF
from django.db import models
from django.utils.text import slugify
from django_extensions.db import fields

class MarkupField(MKF):
    """Let the user chose among different markup types (ReST, Textile, HTML, Markdown)
    default to markdown."""

    pass


class SlugField(fields.AutoSlugField):
    """A custom SlugField that can define his value based on another model field."""
    pass