from django.forms import ModelForm

from . import models, widgets


class BaseMixinForm(ModelForm):

    success_url = "kii:glue:home"
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.request = kwargs.pop('request', None)
        super(BaseMixinForm, self).__init__(*args, **kwargs)


class TitleMixinForm(BaseMixinForm):
    pass

    class Meta:
        model = models.TitleMixin
        fields = ('title',)


class ContentMixinForm(BaseMixinForm):

    class Meta:
        model = models.ContentMixin
        fields = ('content',)
        widgets = {
            'content': widgets.Markdown()
        }


class StatusMixinForm(BaseMixinForm):
    pass

    class Meta:
        model = models.StatusMixin
        fields = ('status',)
