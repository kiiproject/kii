#from markupfield.fields import MarkupField as MKF
from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from django_extensions.db import fields
from django.conf import settings
import markdown


# stolen code from https://github.com/Matt3o12/django-markupfield/blob/master/markupfield/fields.py
# waiting for a fix of https://github.com/jamesturk/django-markupfield/issues/20
class Markdown(object):

    def __init__(self, instance, field_name):
        # instead of storing actual values store a reference to the instance
        # along with field names, this makes assignment possible
        self.instance = instance
        self.field_name = field_name

    # raw is read/write
    def _get_raw(self):
        return self.instance.__dict__[self.field_name]

    def _set_raw(self, val):
        setattr(self.instance, self.field_name, val)

    raw = property(_get_raw, _set_raw)

    markup_type = "markdown"

    # rendered is a read only property
    def _get_rendered(self):
        return getattr(settings, "MARKDOWN_FUNCTION", markdown.markdown)(self.raw)

    rendered = property(_get_rendered)

    # allows display via templates to work without safe filter
    def __unicode__(self):
        return self.raw

    __str__ = __unicode__

class MarkdownDescriptor(object):

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError('Can only be accessed via an instance.')
        markup = instance.__dict__[self.field.name]
        if markup is None:
            return None
        return Markdown(instance, self.field.name)

    def __set__(self, obj, value):
        if isinstance(value, Markdown):
            obj.__dict__[self.field.name] = value.raw
        else:
            obj.__dict__[self.field.name] = value



class MarkdownField(models.TextField):
    """Let the user chose among different markup types (ReST, Textile, HTML, Markdown)
    default to markdown."""

    #right now, classic markupfield is disabled, due to https://github.com/jamesturk/django-markupfield/issues/20
    pass

    def contribute_to_class(self, cls, name):
        super(MarkdownField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, MarkdownDescriptor(self))

class SlugField(fields.AutoSlugField):
    """A custom SlugField that can define his value based on another model field."""
    pass