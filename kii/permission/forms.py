#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import get_anonymous_user

from kii.base_models.forms import BaseMixinForm
from . import models

class PermissionMixinForm(BaseMixinForm):
    
    PERMISSION_CHOICES = (
        ("owner", _("owner")),
        ("everybody",_("everybody")),
    )
    readable_by = forms.ChoiceField(choices=PERMISSION_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = models.PermissionMixin
        fields = ('readable_by', ) 

    def __init__(self, *args, **kwargs):

        super(PermissionMixinForm, self).__init__(**kwargs)

        instance = kwargs.get('instance')

        if instance is not None:
            if instance.readable_by(get_anonymous_user()):
                self.fields['readable_by'].initial = "everybody"
            else:
                self.fields['readable_by'].initial = "owner"

    def save(self, *args, **kwargs):

        readable_by = self.cleaned_data['readable_by']
        if readable_by == "everybody":
            # create required permission object
            self.instance.assign_perm("read", get_anonymous_user())            

        elif readable_by == "owner":
            # Delete anonymous user perm, if any
            self.instance.remove_perm('read', get_anonymous_user())

        return super(PermissionMixinForm, self).save(*args, **kwargs)