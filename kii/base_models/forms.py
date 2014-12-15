from django.forms import ModelForm

from . import models



class BaseMixinForm(ModelForm):
    
    success_url = "kii:glue:home"
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseMixinForm, self).__init__(*args, **kwargs)


class TitleMixinForm(BaseMixinForm):
    pass

    class Meta:
        model = models.TitleMixin
        fields = ('title',)


class ContentMixinForm(BaseMixinForm):
    pass

    class Meta:
        model = models.ContentMixin
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(ContentMixinForm, self).__init__(*args, **kwargs)
        print(self.instance.content.raw)
class StatusMixinForm(BaseMixinForm):
    pass

    class Meta:
        model = models.StatusMixin
        fields = ('status',)

