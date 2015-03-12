from kii.stream import forms

from . import models

class FileForm(forms.StreamItemForm):
    class Meta(forms.StreamItemForm.Meta):        
        model = models.File
        fields = ('file_obj',) + forms.StreamItemForm.Meta.fields

    def __init__(self, *args, **kwargs):
        """By default, files get a low importance because we don't want to pollute users feeds"""
        initial = kwargs.pop('initial')
        if not kwargs.get('instance'):
            initial['importance'] =0
        super(FileForm, self).__init__(*args, initial=initial, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.original_name = self.request.FILES['file_obj'].name
        return super(FileForm, self).save(*args, **kwargs)
        
