from kii.stream import forms

from . import models

class FileForm(forms.StreamItemForm):
    class Meta(forms.StreamItemForm.Meta):        
        model = models.File

        fields = ('file_obj',) + forms.StreamItemForm.Meta.fields