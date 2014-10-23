from django.forms import ModelForm

from . import models



class BaseMixinForm(ModelForm):
    pass


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


class StatusMixinForm(BaseMixinForm):
    pass

    class Meta:
        model = models.StatusMixin
        fields = ('status',)