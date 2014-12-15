from django.db import models
from django.core.urlresolvers import reverse


class AppModel(models.Model):

    # If True, any authenticated user will be able to create isntances of this model
    public_model = False

    def url_namespace(self, **kwargs):
        """Return the URL namespace of the class, such as `app_label:model_label:`"""       

        app_name = self._meta.app_label
        model_name = self.__class__.__name__.lower()

        if kwargs.get('user_area', False):
            prefix = "kii:user_area:"
        else:
            prefix = "kii:"
        return prefix + "{0}:{1}:".format(app_name, model_name)

    def reverse(self, suffix, **kwargs):
        """Return a reversed URL for given suffix (for example: detail, list, edit...)
        you can override per-suffix URLs by defining .reverse_<suffix> methods
        """

        if hasattr(self, 'reverse_{0}'.format(suffix)):
            return getattr(self, 'reverse_{0}'.format(suffix))(**kwargs)  
                      
        return reverse(self.url_namespace(**kwargs) + suffix)
        
    def reverse_detail(self, **kwargs):
        return reverse(self.url_namespace(**kwargs) + "detail", kwargs={"pk":self.pk})

    def reverse_update(self, **kwargs):
        return reverse(self.url_namespace(**kwargs) + "update", kwargs={"pk":self.pk})

    def reverse_delete(self, **kwargs):
        return reverse(self.url_namespace(**kwargs) + "delete", kwargs={"pk":self.pk})

    def get_absolute_url(self):
        return self.reverse_detail(user_include=True)

    @classmethod
    def class_reverse(cls, suffix):
        """Call reverse with an actual instance of the class. Used for reversing if you don't have a class instance"""
        return cls.reverse(cls(), suffix)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.pk)

    class Meta:
        abstract = True