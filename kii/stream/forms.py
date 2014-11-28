from kii.base_models import forms
from . import models


class StreamItemForm(
        forms.TitleMixinForm,
        forms.ContentMixinForm,
        forms.StatusMixinForm,):

    class Meta(
            forms.TitleMixinForm.Meta,
            forms.ContentMixinForm.Meta,
            forms.StatusMixinForm.Meta,):

        model = models.StreamItem
        fields = forms.TitleMixinForm.Meta.fields + \
                 forms.ContentMixinForm.Meta.fields + \
                 forms.StatusMixinForm.Meta.fields + ('root',)


    def __init__(self, *args, **kwargs):
        """Set default stream to user's default stream if no stream is provided"""
        super(StreamItemForm, self).__init__(*args, **kwargs)
        queryset = models.Stream.objects.filter(owner=self.user.pk)
        if len(queryset) < 1:
            raise Exception('User must have at lest one stream')

        self.fields['root'].queryset = queryset
        self.initial['root'] = queryset.first()
        self.fields['root'].empty_label = None
