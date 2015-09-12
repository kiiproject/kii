from kii.base_models import forms
from kii.permission.forms import PermissionMixinForm
from kii.discussion.forms import CommentForm

from . import models


class StreamForm(forms.TitleMixinForm, PermissionMixinForm, forms.ContentMixinForm):

    class Meta(PermissionMixinForm, forms.ContentMixinForm.Meta):
        model = models.Stream
        fields = (forms.TitleMixinForm.Meta.fields +
                  forms.ContentMixinForm.Meta.fields +
                  PermissionMixinForm.Meta.fields)


class StreamItemForm(
        forms.TitleMixinForm,
        forms.ImportanceMixinForm,
        forms.ContentMixinForm,
        forms.StatusMixinForm,):

    class Meta(
            forms.TitleMixinForm.Meta,
            forms.ImportanceMixinForm.Meta,
            forms.ContentMixinForm.Meta,
            forms.StatusMixinForm.Meta,):

        model = models.StreamItem
        fields = (forms.TitleMixinForm.Meta.fields +
                  forms.ContentMixinForm.Meta.fields +
                  forms.StatusMixinForm.Meta.fields +
                  forms.ImportanceMixinForm.Meta.fields +
                  ('root',))

    def __init__(self, *args, **kwargs):
        """Set default stream to user's default stream if no stream is provided
        """

        super(StreamItemForm, self).__init__(*args, **kwargs)
        queryset = models.Stream.objects.filter(owner=self.user.pk)
        if len(queryset) < 1:
            raise Exception('User must have at least one stream')

        self.fields['root'].queryset = queryset
        self.fields['root'].empty_label = None
        if not self.fields['root'].initial:
             self.fields['root'].initial = models.Stream.objects.get(title=self.user.username)



class ItemCommentForm(CommentForm):

    class Meta(CommentForm.Meta):
        model = models.ItemComment
