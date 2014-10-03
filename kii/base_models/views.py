from django.views.generic import DetailView


class ModelTemplateMixin(object):
    """Deduce template_name from model, app and view names"""
    def get_template_names(self):

        if self.template_name:
            # use given template name
            return self.template_name

        app_name = self.model._meta.app_label
        model_name = self.model.__name__.lower()
        template_name = "{0}/{1}/{2}.html".format(app_name, model_name, self.name)

        return [template_name]

class Detail(ModelTemplateMixin, DetailView):
    name = "detail"

    def get_context_object_name(self, obj):
        return "object"