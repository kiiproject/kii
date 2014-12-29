from django import forms as django_forms

import collections

from kii.base_models import forms
from . import models


class CommentForm(forms.ContentMixinForm):    

    class Meta(forms.ContentMixinForm):
        """You will need to set model on child classes"""
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        self.subject = kwargs.pop('subject', None)
        super(CommentForm, self).__init__(*args, **kwargs)

        if not self.request.user.is_authenticated():
            self.build_anonymous_comment_fields()

    def build_anonymous_comment_fields(self):
        # build fields for anonymous comment
        username = django_forms.CharField(max_length=255)
        email = django_forms.EmailField()
        url = django_forms.URLField(required=False)

        anonymous_fields = collections.OrderedDict([
            ('username', username),
            ('email', email),
            ('url', url),
        ])

        # add them at the beginning of the form
        try:
            # python 3
            self.fields = collections.OrderedDict(anonymous_fields.items() | self.fields.items())
        except TypeError:
            # python 2 
            self.fields = collections.OrderedDict(anonymous_fields.items() + self.fields.items())


    def build_anonymous_profile(self):
        profile = models.AnonymousCommenterProfile()
        profile.username = self.cleaned_data['username']
        profile.email = self.cleaned_data['email']
        profile.url = self.cleaned_data['url']

        profile.save()
        return profile

    def save(self, *args, **kwargs):

        self.instance.subject = self.subject

        if self.request.user.is_authenticated():
            self.instance.user = self.request.user
        else:
            self.instance.user_profile = self.build_anonymous_profile()

        return super(CommentForm, self).save(*args, **kwargs)