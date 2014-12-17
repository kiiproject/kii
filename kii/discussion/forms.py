from django import forms as django_forms

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
            self.fields['username'] = django_forms.CharField(max_length=255)
            self.fields['email'] = django_forms.EmailField()
            self.fields['url'] = django_forms.URLField(required=False)

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