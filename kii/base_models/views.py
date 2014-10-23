from django.views.generic import DetailView, ListView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404

from kii.app.views import AppMixin


class RequireAuthenticationMixin(object):
    """Force user authentication before accessing view"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequireAuthenticationMixin, self).dispatch(*args, **kwargs)


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


class ModelFormMixin(RequireAuthenticationMixin, ModelTemplateMixin):

    @classmethod
    def as_view(cls, *args, **kwargs):
        """Deduce model from form class if needed"""
        if kwargs.get('model') is None:
            kwargs['model'] = kwargs.get('form_class').Meta.model
        return super(ModelFormMixin, cls).as_view(*args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ModelFormMixin, self).get_form_kwargs(**kwargs)
        kwargs['user'] = self.request.user
        return kwargs

class Create(ModelFormMixin, CreateView):
    name = "create"

    def get_success_url(self):
        return "/"

class Delete(ModelFormMixin, DeleteView):
    name = "delete"

    def get_success_url(self):
        return "/"


class Detail(ModelTemplateMixin, DetailView):
    name = "detail"

    def get_context_object_name(self, obj):
        return "object"

class List(ModelTemplateMixin, ListView):
    name = "list"
   

class OwnerMixin(object):
    """Deduce owner of given page/elements from url or logged in user"""

    def dispatch(self, request, **kwargs):

        owner_name = kwargs.get('username', None)
        if owner_name is None:
            if request.user.is_authenticated():
                self.owner = request.user

            else:
                if getattr(settings, "KII_DEFAULT_USER", None) is not None:
                    self.owner = get_object_or_404(get_user_model(), username=getattr(settings, "KII_DEFAULT_USER"))
                else:
                    raise Http404
        else:
            self.owner = get_object_or_404(get_user_model(), username=owner_name)

        return super(OwnerMixin, self).dispatch(request, **kwargs) 

    def get_context_data(self, **kwargs):
        context = super(OwnerMixin, self).get_context_data(**kwargs)
        context['owner'] = self.owner
        return context



class OwnerMixinCreate(OwnerMixin, Create):
    """Automatically set model.owner to request.user"""

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerMixinCreate, self).form_valid(form)
    