from django.db import models
from django.core.urlresolvers import reverse


class AppModel(models.Model):
    """
    A base class for all apps related models. It implements URL reversing
    for model instances, so one can do:

    .. code-block:: python

        instance = MyModel.objects.get(pk=42)
        assert instance.reverse_update() == "/kii/myapp/mymodel/42/update"

    """
    #: If True, any authenticated user will be able to create isntances of this model
    # TODO : is it useful ?
    public_model = False

    class Meta:
        abstract = True

    def url_namespace(self, **kwargs):
        """
        :param bool user_area: whether the URL namespace should include the username part
        :return: a string representing the URL namespace of the model, such as ``kii:myapp:mymodel:``"""       

        app_name = self._meta.app_label
        model_name = self.__class__.__name__.lower()

        if kwargs.get('user_area', False):
            prefix = "kii:user_area:"
        else:
            prefix = "kii:"
        return prefix + "{0}:{1}:".format(app_name, model_name)

    def reverse(self, suffix, **kwargs):
        """        
        Get a model-instance relative URL, such as a detail, delete or update URL.
        You can override per-suffix URLs by defining ``reverse_<suffix>`` methods on the model class.

        :param str suffix: a string that will be used to find the corresponding reverse method on the model class (if any)
        :param dict kwargs: optional URL kwargs that will be passed to the reverse function
        :return: a reversed URL 
        """

        if hasattr(self, 'reverse_{0}'.format(suffix)):
            return getattr(self, 'reverse_{0}'.format(suffix))(**kwargs)  
                      
        return reverse(self.url_namespace(**kwargs) + suffix)
        
    def reverse_detail(self, **kwargs):
        """:return: The detail URL of the instance"""
        return reverse(self.url_namespace(**kwargs) + "detail", kwargs={"pk":self.pk})

    def reverse_update(self, **kwargs):
        """:return: The update URL of the instance"""
        return reverse(self.url_namespace(**kwargs) + "update", kwargs={"pk":self.pk})

    def reverse_delete(self, **kwargs):
        """:return: The delete URL of the instance"""
        return reverse(self.url_namespace(**kwargs) + "delete", kwargs={"pk":self.pk})

    def get_absolute_url(self):
        """:return: The absolute URL of the instance, which is equal to ``self.reverse_detail()`` by default"""
        # TODO : user_include should be replaced with user_area
        return self.reverse_detail(user_include=True)

    @classmethod
    def class_reverse(cls, suffix):
        """Same as ``reverse`` but callable from class instead of instances.
        
        :return: a reversed URL for the model"""
        return cls.reverse(cls(), suffix)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.pk)