from django.db import models
from django.core.urlresolvers import reverse


class AppModel(models.Model):

    # If True, any authenticated user will be able to create isntances of this model
    public_model = False

    @property
    def url_namespace(self):
        """Return the URL namespace of the class, such as `app_label:model_label:`"""       

        app_name = self._meta.app_label
        model_name = self.__class__.__name__.lower()

        return "kii:{0}:{1}:".format(app_name, model_name)

    def reverse(self, suffix):
        """Return a reversed URL for given suffix (for example: detail, list, edit...)
        you can override per-suffix URLs by defining .reverse_<suffix> methods
        """

        if hasattr(self, 'reverse_{0}'.format(suffix)):
            return getattr(self, 'reverse_{0}'.format(suffix))()  
                      
        return reverse(self.url_namespace + suffix)
        
    def reverse_detail(self):
        return reverse(self.url_namespace + "detail", kwargs={"pk":self.pk})

    def reverse_update(self):
        return reverse(self.url_namespace + "update", kwargs={"pk":self.pk})

    def reverse_delete(self):
        return reverse(self.url_namespace + "delete", kwargs={"pk":self.pk})

    def get_absolute_url(self):
        return self.reverse_detail()

    @classmethod
    def class_reverse(cls, suffix):
        """Call reverse with an actual instance of the class. Used for reversing if you don't have a class instance"""
        return cls.reverse(cls(), suffix)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.pk)

    class Meta:
        abstract = True