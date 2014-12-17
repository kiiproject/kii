from kii.base_models import forms

class CommentForm(forms.ContentMixinForm):    

    def __init__(self, *args, **kwargs):
        self.subject = kwargs.pop('subject', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        
    class Meta(forms.ContentMixinForm):
        """You will need to set model on child classes"""
        fields = ('content',)

    def save(self, *args, **kwargs):

        self.instance.subject = self.subject
        if self.request.user.is_authenticated():
            self.instance.user = self.request.user

        return super(CommentForm, self).save(*args, **kwargs)