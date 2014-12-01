from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from kii.app.views import AppMixin
from . import forms


class RequireAuthenticationMixin(object):
    """Force user authentication before accessing view"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequireAuthenticationMixin, self).dispatch(*args, **kwargs)


class ModelTemplateMixin(AppMixin):
    def get_template_names(self):
        """Deduce template_name from model name, app name and action"""

        if self.template_name:
            # use given template name
            return self.template_name

        return self.model.get_template_names(self.action)

    def get_context_data(self, **kwargs):

        context = super(ModelTemplateMixin, self).get_context_data(**kwargs)
        context["model"] = self.model
        context["action"] = self.action
        return context


class ModelFormMixin(ModelTemplateMixin):

    form_template = "base_models/modelform.html"
    @classmethod
    def as_view(cls, *args, **kwargs):
        """Deduce model from form class if needed"""
        if getattr(cls, "model", None) is None and kwargs.get('model') is None:
            form_class = kwargs.get('form_class', getattr(cls, "form_class"))
            kwargs['model'] = form_class.Meta.model
        return super(ModelFormMixin, cls).as_view(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModelFormMixin, self).get_context_data(**kwargs)
        context['form_template'] = self.form_template
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ModelFormMixin, self).get_form_kwargs(**kwargs)
        if self.form_class is not None and issubclass(self.form_class, forms.BaseMixinForm):
            kwargs['user'] = self.request.user
        return kwargs

class Create(ModelFormMixin, CreateView):
    action = "create"


class Update(ModelFormMixin, UpdateView):
    action = "update"


class Delete(DeleteView):
    action = "delete"

    def get_success_url(self):
        return reverse("kii:glue:home")


class Detail(ModelTemplateMixin, DetailView):
    action = "detail"

    def get_context_object_name(self, obj):
        return "object"

class List(ModelTemplateMixin, ListView):
    action = "list"
   

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


class OwnerMixinDetail(OwnerMixin, Detail):
    pass

class OwnerMixinList(OwnerMixin, List):
    pass

class OwnerMixinCreate(RequireAuthenticationMixin, Create, OwnerMixin):
    """Automatically set model.owner to request.user"""

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerMixinCreate, self).form_valid(form)


class RequireOwnerMixin(RequireAuthenticationMixin):
    """Requires request.user to be owner of the model instance"""

    def get_object(self, **kwargs):
        obj = super(RequireOwnerMixin, self).get_object(**kwargs)

        if not obj.owned_by(self.request.user):
            raise PermissionDenied()

        return obj
    
class OwnerMixinUpdate(RequireOwnerMixin, Update, OwnerMixin):
    pass

class OwnerMixinDelete(RequireOwnerMixin, Delete, OwnerMixin):

    template_name = "base_models/basemixin/delete.html"