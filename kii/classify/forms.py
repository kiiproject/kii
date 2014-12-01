from kii.base_models import forms
from . import models


class TagForm(forms.TitleMixinForm):

    class Meta(forms.TitleMixinForm.Meta):

        model = models.Tag
        fields = forms.TitleMixinForm.Meta.fields

