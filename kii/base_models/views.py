from django.views.generic import DetailView, ListView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from kii.app.views import AppMixin

class ModelTemplateMixin(AppMixin):
    def get_template_names(self):
        """Deduce template_name from model, app and view names"""

        if self.template_name:
            # use given template name
            return self.template_name

        return self.model.get_template_names(self.name)

    def get_context_data(self, **kwargs):

        context = super(ModelTemplateMixin, self).get_context_data(**kwargs)
        context["model"] = self.model
        return context

class Create(ModelTemplateMixin, CreateView):
    name = "create"

    def get_success_url(self):
        return "/"

class Delete(ModelTemplateMixin, DeleteView):
    name = "delete"

    def get_success_url(self):
        return "/"


class Detail(ModelTemplateMixin, DetailView):
    name = "detail"

    def get_context_object_name(self, obj):
        return "object"

class List(ModelTemplateMixin, ListView):
    name = "list"
   

class RequireAuthenticationMixin(object):
    """Force user authentication before accessing view"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequireAuthenticationMixin, self).dispatch(*args, **kwargs)


class OwnerMixinCreate(RequireAuthenticationMixin, Create):
    """Automatically set model.owner to request.user"""

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerMixinCreate, self).form_valid(form)
    