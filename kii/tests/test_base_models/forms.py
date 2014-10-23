from kii.base_models import forms
from . import models

class ContentModelForm(forms.ContentMixinForm):

    class Meta(forms.ContentMixinForm.Meta):
        model = models.ContentModel

class OwnerModelForm(forms.BaseMixinForm):

    class Meta:
        model = models.OwnerModel