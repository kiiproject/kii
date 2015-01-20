from kii.stream import forms

from . import models

class FileForm(forms.StreamItemForm):
    class Meta(forms.StreamItemForm.Meta):        
        model = models.File
        fields = ('file_obj',) + forms.StreamItemForm.Meta.fields

    def save(self, *args, **kwargs):
        self.instance.original_name = self.request.FILES['file_obj'].name
        return super(FileForm, self).save(*args, **kwargs)